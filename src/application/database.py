from src.application.input import read_input_file
import json
import os
database_file = 'database.json'
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, database_file)


class Database:
    def create_database(self):
        cards = read_input_file('example_words.csv') # get cards from the input function
        with open(database_file, 'w') as f:
            json.dump([obj.__dict__ for obj in cards], f)

    def get_cards(self):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data


database = Database()
database.create_database()
