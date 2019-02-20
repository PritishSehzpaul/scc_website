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


def validateOTP(request, otp):
    otp_entered = request.form.get('otp')
    if otp_entered is not None:
        try:
            otp_entered = int(otp_entered)
            if otp == otp_entered:
                return True
            else:
                return False
        except ValueError as e:
            print('{} cannot be converted to integer. Entered value contains a character.\nError: {}'
                  .format(otp_entered, e))
            return False


def addUser(request=None, session=None):
    if request is None or session is None:
        return None
    else:
        session['sid'] = request.form.get('sid').strip()
        session['name'] = request.form.get('name').strip()
        session['email'] = request.form.get('email').strip()
        session['contact'] = request.form.get('contact').strip()


def removeUser(session=None):
    if session is None:
        return None

    del session['sid']
    del session['email']
    del session['contact']
    del session['name']
    del session['otp_validated']
    del session['otp_sent']

    print('REMOVE USER FUNCTION\n\n')
    print('otp_sent' in session)
    print('\n\n')

