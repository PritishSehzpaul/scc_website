"""
backend.py file containing functions that perform operations on data
"""
import random

def calc_score(request=None):
    """
    Calculates the score of a student who takes the questionnaire
    :return: a map with 3 keys i.e. 'stress', 'anxiety', 'depression' where key is string and value is int (score)
    """

    stress_set = [1, 6, 8, 11, 12, 14, 18]
    anxiety_set = [2, 4, 7, 9, 15, 19, 20]
    depression_set = [3, 5, 10, 13, 16, 17, 21]
    # question_set = {'stress': stress_set, 'anxiety': anxiety_set, 'depression': depression_set}
    selected_option_set = []
    score_set = {'stress': 0, 'anxiety': 0, 'depression': 0}

    for i in range(1, 22):
        if request.form.get('group-' + str(i)) is None:
            val = 0
        else:
            val = int(request.form.get('group-' + str(i)))

        selected_option_set.append(val)
        if i in stress_set:
            score_set['stress'] += val
        elif i in anxiety_set:
            score_set['anxiety'] += val
        else:
            score_set['depression'] += val

    return score_set


def generateOTP():
    return random.SystemRandom().randint(100000, 999999)
