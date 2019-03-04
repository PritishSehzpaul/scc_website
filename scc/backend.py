"""
backend.py file containing functions that perform operations on data
"""
import random
import hashlib

from config.app_logger import AppLogger

# Set logger
logger = AppLogger(__name__, AppLogger.DEBUG).logger

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


def validateOTP(request, hash_otp, salt):
    otp_entered = request.form.get('otp')
    logger.info('Validating OTP...')
    if otp_entered is not None:
        try:
            otp_entered = int(otp_entered)
            hash_otp_entered = encrypt(otp_entered, salt)
            if hash_otp == hash_otp_entered:
                logger.info('OTP is correct')
                return True
            else:
                logger.info('OTP is incorrect')
                return False
        except ValueError as e:
            logger.exception('OTP entered is: ' + otp_entered + '{} cannot be converted to integer'.format(otp_entered))
            return False


def addUser(request=None, session=None):
    if request is None or session is None:
        return None
    else:
        session['sid'] = request.form.get('sid').strip()
        session['name'] = request.form.get('name').strip()
        session['email'] = request.form.get('email').strip()
        session['contact'] = request.form.get('contact').strip()
        session['otp_retry_count'] = 0
        session['on_form_page'] = False


def removeUser(session=None):
    if session is None:
        return None

    session.clear()


# TODO further look into key derivation algorithms like : pbkdf2_hmac, BLAKE
def encrypt(s, salt):
    h = hashlib.sha256()
    h.update( str(s+salt).encode('utf-8') )
    return h.hexdigest()


## Might be used in future when we have better translation between webpage and pdf. Not to be used until then
# def convertFormToPDF(url, session):
#     options = {
#         'page-size': 'A4',
#         'margin-top': '0.75in',
#         'margin-right': '0.75in',
#         'margin-bottom': '0.75in',
#         'margin-left': '0.75in',
#     }
#
#     if 'windows' == platform.system().lower():
#         wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # while running on windows change this path
#         config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
#         pdfkit.from_url(url, 'static/submissions/' + session['sid'] + '.pdf', options=options, configuration=config)
#     else:
#         pdfkit.from_url(url, 'static/submissions/' + session['sid'] + '.pdf', options=options)

