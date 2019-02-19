import backend
import mailing
from config.configuration import Configuration
from flask import Flask, render_template, redirect, url_for, request, session


app = Flask('scc')


# initializing config variables
config = Configuration().config
app.secret_key = config['secret_key']   # secret_key for session management

# routes for webpages
LOGIN = 'login'                 # login         --> /login/
OTP = 'otp'                     # otp           --> /otp/
DASS21 = 'dass21'               # dass21        --> /dass21/
SUCCESSFUL = 'successful'       # sucessful     --> /sucessful/
UNSUCCESSFUL = 'unsuccessful'   # unsuccessful  --> /unsuccessful/
SUBMISSION = 'submission'       # submission    --> /submission/

# global variables
otp_generated = None

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
    return render_template('index.html', OTP=OTP)


@app.route(__create_URL(OTP), methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        global otp_generated    # TODO remove the global variable and send the information via the url arguments

        backend.addUser(request, session)
        print('\nOver here in otp\n\n')
        print('otp_sent' in session)    # TODO this is coming out True. So this bug has to be removed. otp_sent is a problem
        print('\n\n')
        otp_generated = backend.generateOTP()
        mailing.mailOTP(session=session, otp=otp_generated)

        session['otp_sent'] = True

        return render_template('otp.html', DASS21=DASS21)
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(DASS21), methods=['GET', 'POST'])
def dass21():
    if request.method == 'POST':
        # TODO ask Sonali how can we get through the issue of validating otp without having to render otp page again
        is_otp_correct = backend.validateOTP(request, otp_generated)
        if is_otp_correct:
            session['otp_validated'] = True
            return render_template('dass21.html', SUBMISSION=SUBMISSION)
        else:
            return redirect(url_for(OTP), code=307)
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(SUBMISSION), methods=['GET', 'POST'])
def submission():
    if request.method == 'POST':

        try:
            admin_email = config['mailing']['admin_email']
            score_set = backend.calc_score(request=request)
            comments = request.form.get('comments')
            mailing.mailScore(session=session, recipient=admin_email, score_set=score_set,
                              comments=comments, subject='Score of Student')

            return redirect(url_for('suc_submission'), code=307)    # error code 307 will use the method
            # originallly used for the route which calls redirect

        except Exception as exception:
            print(exception)
            print(type(exception))
            return redirect(url_for('unsuc_submission'), code=307)

    else:
        redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(SUCCESSFUL), methods=['GET', 'POST'])
def suc_submission():
    backend.removeUser(session)

    if request.method == 'POST':
        return render_template('suc_submission.html')
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(UNSUCCESSFUL), methods=['GET', 'POST'])
def unsuc_submission():
    backend.removeUser(session)

    if request.method == 'POST':
        return render_template('unsuc_submission.html')
    else:
        return redirect(url_for(LOGIN), code=302)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
