'''
main.py file containing views
'''
from flask import Flask, render_template, redirect, url_for, request, session


from config.app_logger import AppLogger
# create logs directory. has to be before all the imports because AppLoader is instantiated
AppLogger.ensure_log_dir()

import backend
import mailing
from config.configuration import Configuration


# Set config
config = Configuration().config

# Set logger.
logger = AppLogger(__name__, AppLogger.DEBUG).logger

# Set app
logger.info("Initializing app...")
app = Flask(__name__)
app.secret_key = config['secret_key']   # secret_key for securely signing the cookie so that it can't be changed
logger.info("App initialized")

# Set routes
LOGIN = 'login'                 # login         --> /login/
OTP = 'otp'                     # otp           --> /otp/
DASS21 = 'dass21'               # dass21        --> /dass21/
SUCCESSFUL = 'successful'       # sucessful     --> /sucessful/
UNSUCCESSFUL = 'unsuccessful'   # unsuccessful  --> /unsuccessful/
SUBMISSION = 'submission'       # submission    --> /submission/

# TODO prevent site from going back after details have been entered


def __create_URL(uri):
    return '/' + uri + '/'


@app.route('/', methods=['GET', 'POST'])
def index():
    # Setting session lifetime
    session.permanent = False

    return redirect(url_for(LOGIN), code=303)  # because 303 Used to redirect after a PUT or a POST to prevent a refresh
    #  of the page that would re-trigger the operation. GET methods unchanged.
    # Others changed to GET (body lost).


@app.route(__create_URL(LOGIN), methods=['GET', 'POST'])
def login():
    if 'otp_retry_count' in session and session['otp_retry_count'] > 0:
        logger.warning('Redirecting from \login\ to \otp\ as user is in session. \nSession: ' + repr(session))
        return redirect(url_for(OTP, otp_retry_count=session['otp_retry_count']), code=303)
    elif 'on_form_page' in session and session['on_form_page'] is True:
        logger.warning('Redirecting from \login\ to \dass21\ form as user is in session. \nSession: ' + repr(session))
        return redirect(url_for(DASS21), code=303)

    return render_template('index.html', OTP=OTP)


#TODO mail otp asynchronously

@app.route(__create_URL(OTP), methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':

        if 'otp_retry_count' in session and session['otp_retry_count'] > 0:
            return render_template('otp.html', DASS21=DASS21)
        else:
            logger.info('Creating user session...')
            backend.addUser(request, session)
            logger.info('User session created')
            logger.info('Generating and mailing OTP...')
            otp_gen = backend.generateOTP()
            salt = config['salt']
            session['otp'] = backend.encrypt(otp_gen, salt)
            mailing.mailOTP(session=session, otp=otp_gen)
            session['otp_sent'] = True
            logger.info('OTP mailed.')

            return render_template('otp.html', DASS21=DASS21)
    else:
        if 'otp_retry_count' in session and session['otp_retry_count'] > 0:
            logger.warning('User is in session and loaded the /otp/ page using GET (from browser). \nSession: ' + repr(session))
            return render_template('otp.html', DASS21=DASS21)

        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(DASS21), methods=['GET', 'POST'])
def dass21():
    if request.method == 'POST':
        if 'otp' in session:    # otp will always be in session because there is no path otherwise\
            is_otp_correct = backend.validateOTP(request, session['otp'], salt=config['salt'])
            if is_otp_correct:
                session['otp_validated'] = True
                session['otp_retry_count'] = 0  # reset otp_retry_count
                session['on_form_page'] = True
                logger.info('Opening \dass21\ form page...')
                return render_template('dass21.html', SUBMISSION=SUBMISSION)
            else:
                session['otp_retry_count'] += 1
                logger.info('Redirecting from \dass21\ to \otp\ as OTP is incorrect. \nSession: ' + repr(session))
                return redirect(url_for(OTP, otp_retry_count=session['otp_retry_count']), code=307)
    else:
        if 'on_form_page' in session and session['on_form_page'] is True:
            logger.warning('User is in session and loaded \dass21\ using GET (from browser). \nSession: ' + repr(session))
            return render_template('dass21.html', SUBMISSION=SUBMISSION)

        return redirect(url_for(LOGIN), code=302)


#TODO check the routes when the POST is not used

@app.route(__create_URL(SUBMISSION), methods=['GET', 'POST'])
def submission():
    if request.method == 'POST':

        session['on_form_page'] = False

        try:
            admin_email = config['mailing']['admin_email']
            score_set = backend.calc_score(request=request)
            comments = request.form.get('comments')
            logger.info('Mailing result to admin')
            mailing.mailScore(session=session, recipient=admin_email, score_set=score_set,
                              comments=comments, subject='Score of Student')
            logger.info('User submission is successful. Result mailed')
            return redirect(url_for('suc_submission'), code=307)    # code 307 will use the method originally used
            # for the route which calls redirect

        except Exception as exception:
            logger.exception('User submission unsuccessful. Result not mailed')
            return redirect(url_for('unsuc_submission'), code=307)

    else:
        logger.warning('Redirecting from \submission\ to \login\ as user accessed route using GET')
        redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(SUCCESSFUL), methods=['GET', 'POST'])
def suc_submission():

    if request.method == 'POST':
        if 'sid' in session:
            logger.info('Removing user from session. \nSession: ' + repr(session))
            backend.removeUser(session)
            logger.info('User removed')
        return render_template('suc_submission.html')
    else:
        logger.warning('Redirecting from \successful\ to \login\ as user accessed route using GET')
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(UNSUCCESSFUL), methods=['GET', 'POST'])
def unsuc_submission():

    if request.method == 'POST':
        if 'sid' in session:
            logger.info('Removing user from session. \nSession: ' + repr(session))
            backend.removeUser(session)
            logger.info('User removed')
        return render_template('unsuc_submission.html')
    else:

        logger.warning('Redirecting from \\unsuccessful\ to \login\ as user accessed route using GET')
        return redirect(url_for(LOGIN), code=302)


@app.errorhandler(404)
def page_not_found(err):
    logger.error('Page not found. Request url: ' + request.url)
    return render_template('page_not_found.html'), 404



# if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=5000)

# TODO: Add a close button on the form in dass21 page
# TODO: ask sonali to change the checking of entries in input fields to per character: make it aggressive