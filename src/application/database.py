from src.application.input import read_input_file
import json
import os


class Database:
    _database_file = 'database.json'

    def create_database(self):
        cards = read_input_file('example_words.csv') # get cards from the input function
        with open(self._get_database_file_path(), 'w') as f:
            json.dump([obj.__dict__ for obj in cards], f)

    def get_cards(self):
        file_path = self._get_database_file_path()
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data

    def _get_database_file_path(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, self._database_file)
        return file_path


# database = Database()
# database.create_database()
