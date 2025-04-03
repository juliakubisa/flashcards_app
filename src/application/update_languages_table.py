from src.domain.language import Language
import os


def read_languages():
    languages = []
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'premade_data/lang.csv')
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            lang_code = line.split(',')[0].strip()
            lang_name = line.split(',')[1].strip()
            language = Language(lang_code=lang_code, lang_name=lang_name)
            languages.append(language)
    return languages


def insert_languages(db_session):
    if len(db_session.query(Language).all()) == 0:
        languages = read_languages()
        db_session.add_all(languages)
        db_session.commit()
