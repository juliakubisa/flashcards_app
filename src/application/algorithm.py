import statistics


class AlgorithmVariables:
    """Specifies  the variables that will be used in the algorithm"""
    def __init__(self):
        self.days_since_last_review = 0
        self.number_correct_answers = 0
        self.answer_time = 0


class Algorithm:
    """easiness = -A*days_since_last_review + B*last_review_correct +
            C*number_correct_answers + D*answer_time
        where A, B, C, D are weights"""
    def __init__(self):
        self.easiness_factor = 0

    def set_weights(self, card, cards):
        values = self.standarize_values(card, cards)
        last_answer_correct = -1 if not card.last_answer_correct else 1

        days_since_last_review_weight = -0.25
        last_answer_correct_weight = 0.25
        number_correct_answers_weight = 0.25
        answer_time_weight = -0.25

        self.easiness_factor = (last_answer_correct_weight * last_answer_correct
                                + number_correct_answers_weight * values.number_correct_answers
                                + answer_time_weight * values.answer_time)
        card.easiness_factor = self.calculate_new_easiness(card)

    def standarize_values(self, card, cards):
        algorithm_variables = AlgorithmVariables()
        variables_names = algorithm_variables.__dict__.keys()

        for name in variables_names:
            std_val = statistics.stdev((getattr(c, name) for c in cards))
            mean_val = statistics.mean((getattr(c, name) for c in cards))
            setattr(algorithm_variables, name, ((getattr(card, name) - std_val) / mean_val))
        return algorithm_variables

    def calculate_new_easiness(self, card):
        current_easiness = card.easiness_factor
        new_easiness_factor = self.easiness_factor
        return new_easiness_factor

