from datetime import date
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.model.cards_to_quiz_dto import QuizCardDTO
from difflib import get_close_matches
import random
import warnings
warnings.filterwarnings("ignore")


class Algorithm:
    """easiness = -A*days_since_last_review + B*last_review_correct +
            C*number_correct_answers + D*answer_time
        where A, B, C, D are weights"""

    def __init__(self, cards, num_cards):
        self.df = pd.DataFrame([c.__dict__ for c in cards])  # Convert Card objects to pandas dataframe
        self.num_cards = num_cards
        self.standarize_variables_list = ['days_since_last_review', 'number_correct_answers', 'answer_time']
        self.standarized_variables_list = ['days_since_last_review_s', 'number_correct_answers_s', 'answer_time_s']

    def set_weights(self):
        # The cards that were quizzed before
        old_entries = self.df['date_last_review'].notna()

        if old_entries.any():
            # Modify only the quizzed cards
            self.df.loc[old_entries, 'last_answer_correct'] = np.where(self.df.loc[old_entries, 'last_answer_correct'] is False, 1, -1)
            self.df.loc[old_entries, 'days_since_last_review'] = abs((self.df.loc[old_entries, 'date_last_review']
                                                                      - date.today()).apply(lambda d: d.days))
            self.standarize_values(old_entries)

            weights = [0.25, 0.25, -0.25, -0.25]
            self.df.loc[old_entries, 'new_easiness'] = (weights[0] * self.df.loc[old_entries, 'last_answer_correct']
                                       + weights[1] * self.df.loc[old_entries, 'number_correct_answers_s']
                                       + weights[2] * self.df.loc[old_entries, 'answer_time_s']
                                       + weights[3] * self.df.loc[old_entries, 'days_since_last_review'])

    def standarize_values(self, old_entries):
        """Z = (X − µ)/σ where X is the variable, µ is the column mean and σ is column standard deviation"""
        scaler = StandardScaler()
        self.df.loc[old_entries, self.standarized_variables_list] =\
            scaler.fit_transform(self.df.loc[old_entries, self.standarize_variables_list])

    def adjust_easiness(self, old_entries_df):
        """Apply algorithmic mean between old and new easiness factor to adjust it
        where adjusted_easiness = 1/2(old_easiness+new_easiness)"""
        old_entries_df.loc[old_entries_df['new_easiness'] < 0, 'new_easiness'] = 0
        old_entries_df['easiness_factor'] = round((old_entries_df['easiness_factor'] + old_entries_df['new_easiness']) / 2, 3)
        return old_entries_df

    def select_quiz_cards(self):
        new_entries_df, old_entries_df = self.select_new_entries()

        if len(old_entries_df) == 0:
            cards_to_quiz_ids = np.random.choice(new_entries_df['id'], self.num_cards, replace=False).tolist()
            cards_to_quiz_df = new_entries_df[new_entries_df['id'].isin(cards_to_quiz_ids)]
        else:
            old_entries_df = self.adjust_easiness(old_entries_df)
            old_entries_df['probability'] = (old_entries_df['easiness_factor'] / old_entries_df['easiness_factor'].sum())

            if len(old_entries_df) < 0.8 * self.num_cards:
                old_entries_to_quiz_ids = np.random.choice(old_entries_df['id'], len(old_entries_df), replace=False).tolist()
                new_entries_to_quiz_ids = np.random.choice(new_entries_df['id'], self.num_cards - len(old_entries_to_quiz_ids),
                                                           replace=False).tolist()

            elif len(old_entries_df) > 0.8 * self.num_cards and len(new_entries_df) > 0.2:
                old_entries_to_quiz_ids = np.random.choice(old_entries_df['id'], round(0.8 * self.num_cards),
                                                           p=old_entries_df['probability'], replace=False).tolist()
                new_entries_to_quiz_ids = np.random.choice(new_entries_df['id'], self.num_cards -
                                                           len(old_entries_to_quiz_ids), replace=False).tolist()

            else:
                new_entries_to_quiz_ids = np.random.choice(new_entries_df['id'], len(new_entries_df), replace=False).tolist()
                old_entries_to_quiz_ids = np.random.choice(old_entries_df['id'], self.num_cards - len(new_entries_to_quiz_ids),
                                                           p=old_entries_df['probability'], replace=False).tolist()

            old_entries_to_quiz_df = old_entries_df[old_entries_df['id'].isin(old_entries_to_quiz_ids)]
            new_entries_to_quiz_df = new_entries_df[new_entries_df['id'].isin(new_entries_to_quiz_ids)]
            cards_to_quiz_df = pd.concat([new_entries_to_quiz_df, old_entries_to_quiz_df])

        similar_answers_df = self.select_similar_cards(cards_to_quiz_df['foreign_word'].to_list())
        cards_to_quiz_with_answers_df = (pd.merge(cards_to_quiz_df, similar_answers_df, on='foreign_word'))

        self.df['last_answer_correct'] = self.df['last_answer_correct'].astype(bool)
        return self._df_to_cards_list(cards_to_quiz_with_answers_df)

    def select_similar_cards(self, words):
        """Selects 3 other options for quiz ABCD mode"""
        similar_answers = []
        all_foreign_words = self.df['foreign_word']

        for word in words:
            other_words = all_foreign_words[all_foreign_words != word]
            similar_words = get_close_matches(word, other_words.to_list(), 3)

            # If difflib cannot find all 3 similar answers manually append random
            while len(similar_words) < 3:
                similar_words.extend(random.sample(other_words.to_list(), 3-len(similar_words)))
            similar_answers.append([word, similar_words])

        similar_answers_df = pd.DataFrame(similar_answers, columns=['foreign_word', 'similar_words'])
        return similar_answers_df

    def select_new_entries(self):
        """Distinguish between new cards (never seen before) and old cards"""
        new_entries_df = self.df[self.df['date_last_review'].isnull()]
        old_entries_df = self.df[~self.df['date_last_review'].isnull()]
        return new_entries_df, old_entries_df

    def _df_to_cards_list(self, df):
        return [
            QuizCardDTO(row['id'], row['foreign_word'], row['translated_word'], row['similar_words'])
            for index, row in df.iterrows()
        ]
