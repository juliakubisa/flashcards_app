from datetime import date
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.model.cards_to_quiz_dto import QuizCardDTO
from difflib import get_close_matches
import random


class Algorithm:
    """easiness = -A*days_since_last_review + B*last_review_correct +
            C*number_correct_answers + D*answer_time
        where A, B, C, D are weights"""

    def __init__(self, cards):
        self.df = pd.DataFrame([c.__dict__ for c in cards])  # Convert Card objects to pandas dataframe
        self.standarize_variables_list = ['days_since_last_review', 'number_correct_answers', 'answer_time']
        self.standarized_variables_list = ['days_since_last_review_s', 'number_correct_answers_s', 'answer_time_s']

    def set_weights(self):
        self.df['last_answer_correct'] = np.where(self.df['last_answer_correct'] is False, 1, -1)
        self.df['days_since_last_review'] = (self.df['date_last_review'] - date.today()).apply(lambda d: d.days)
        self.standarize_values()
        weights = [-0.25, 0.25, 0.25, -0.25, 0.25]

        self.df['new_easiness'] = (weights[1] * self.df['last_answer_correct']
                                   + weights[2] * self.df['number_correct_answers_s']
                                   + weights[3] * self.df['answer_time_s']
                                   + weights[4] * self.df['days_since_last_review'])

    def standarize_values(self):
        """Z = (X − µ)/σ where X is the variable from list, µ is the column mean and σ is column standard deviation"""
        scaler = StandardScaler()
        self.df[self.standarized_variables_list] = scaler.fit_transform(self.df[self.standarize_variables_list])

    def adjust_easiness(self):
        """Apply algorithmic mean between old and new easiness factor to adjust it
        where adjusted_easiness = 1/2(old_easiness+new_easiness)"""
        self.df.loc[self.df['new_easiness'] < 0, 'new_easiness'] = 0
        self.df['easiness_factor'] = round((self.df['easiness_factor'] + self.df['new_easiness']) / 2, 3)

    def select_quiz_cards(self):
        self.adjust_easiness()
        self.df['probability'] = (self.df['easiness_factor'] / self.df['easiness_factor'].sum())
        cards_to_quiz_ids = np.random.choice(self.df['id'], 20, p=self.df['probability']).tolist()
        cards_to_quiz_df = self.df[self.df['id'].isin(cards_to_quiz_ids)]

        similar_answers_df = self.select_similar_cards(cards_to_quiz_df['foreign_word'].to_list())
        cards_to_quiz_with_answers_df = (pd.merge(cards_to_quiz_df, similar_answers_df, on='foreign_word'))

        self.df['last_answer_correct'] = np.where(self.df['last_answer_correct'] == 1, True, False)
        return self._df_to_cards_list(cards_to_quiz_with_answers_df)

    def select_similar_cards(self, words):
        """Selects 3 other options for quiz ABCD mode"""
        similar_answers = []
        possible_answers = self.df[~self.df['foreign_word'].isin(words)]['foreign_word']
        possible_answers = possible_answers.to_list()
        for word in words:
            similar_words = get_close_matches(word, possible_answers, 3)

            # If difflib cannot find all 3 similar answers manually append random
            while len(similar_words) < 3:
                similar_words.extend(random.sample(possible_answers, 3-len(similar_words)))
            similar_answers.append([word, similar_words])

        similar_answers_df = pd.DataFrame(similar_answers, columns=['foreign_word', 'similar_words'])
        return similar_answers_df

    def _df_to_cards_list(self, df):
        return [
            QuizCardDTO(row['id'], row['foreign_word'], row['translated_word'], row['similar_words'])
            for index, row in df.iterrows()
        ]
