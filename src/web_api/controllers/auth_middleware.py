from flask import current_app, jsonify, request
import jwt


def check_authentication():
    if request.blueprint == 'account_controller':
        return None

    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({"message": "No Authorization header present"}), 401

    token = auth_header.split(" ")[1] if " " in auth_header else None

    if not token:
        return jsonify({"message": "Invalid Authorization header"}), 401

    try:
        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 403

    return None