import datetime
import os
from flask import Blueprint, jsonify, request, current_app
from src.application.sql_database import db
from src.model.account import Account 
import jwt
import bcrypt
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
import secrets
import string


account_controller = Blueprint('account_controller', __name__)

@account_controller.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not name or not email or not password:
        return jsonify({"message": "Name, email and password are required"}), 400

    account_duplicates_count = db.session.query(Account).filter(Account.email == email).count()

    if account_duplicates_count > 0:
        return jsonify({"message": "Account with such email already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    
    new_account = Account(name, email, hashed_password)

    db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "Account registered successfully"}), 201


@account_controller.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    account = db.session.query(Account).filter(Account.email == email).scalar()

    if not account or not bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
        return jsonify({"message": "Email or password invalid"}), 404

    access_token = generate_access_token(email)
    refresh_token = generate_refresh_token(email)

    account.refresh_token = refresh_token
    db.session.commit()

    return jsonify({"message": "Successful login", "access_token": access_token, "refresh_token": refresh_token, "email": email, "name": account.name}), 200

@account_controller.route('/login_with_google', methods=['POST'])
def login_with_google():
    try:
        google_credential = request.json.get('idToken')
        payload = google_id_token.verify_oauth2_token(google_credential, google_requests.Request(), current_app.config['GOOGLE_CLIENT_ID'])
    except ValueError:
        return jsonify({"message": "Invalid token"}), 401
    
    user_google_id = payload['sub']
    user_email = payload['email']

    account = db.session.query(Account).filter(Account.google_id == user_google_id).scalar()

    if not account:
        account = Account(payload['name'], user_email, generate_random_password())
        account.google_id = user_google_id
        db.session.add(account)
        db.session.commit()
    
    access_token = generate_access_token(user_email)
    refresh_token = generate_refresh_token(user_email)

    account.refresh_token = refresh_token
    db.session.commit()

    return jsonify({"message": "Successful login", "access_token": access_token, "refresh_token": refresh_token, "email": user_email, "name": account.name}), 200

@account_controller.route('/refresh_token', methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')

    if not refresh_token:
        return jsonify({"message": "Refresh token is required"}), 400
    
    try:
        decoded_token = jwt.decode(refresh_token, current_app.config['JWT_SECRET'], algorithms=['HS256'])

        email = decoded_token['email']

        account = db.session.query(Account).filter(Account.email == email and Account.refresh_token == refresh_token).scalar()

        if not account:
            return jsonify({"message": "Invalid refresh token"}), 403

        new_access_token = generate_access_token(email)
        new_refresh_token = generate_refresh_token(email)

        account.refresh_token = new_refresh_token
        db.session.commit()

        return jsonify(access_token=new_access_token, refresh_token=new_refresh_token), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 403
    

def generate_access_token(email):
    token_payload = {
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10),
        'token_type': 'access'
    }
    
    token = jwt.encode(token_payload, current_app.config['JWT_SECRET'], algorithm='HS256')

    return token

def generate_refresh_token(email):
    token_payload = {
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30),
        'token_type': 'refresh'
    }
    
    token = jwt.encode(token_payload, current_app.config['JWT_SECRET'], algorithm='HS256')

    return token

def generate_random_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password