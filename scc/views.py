import backend
import mailing
from flask import Flask, render_template, redirect, url_for, request

app = Flask('scc')

###  routes for webpages
LOGIN = 'login'                 # login         --> /login/
OTP = 'otp'                     # otp           --> /otp/
DASS21 = 'dass21'               # dass21        --> /dass21/
SUCCESSFUL = 'successful'       # sucessful     --> /sucessful/
UNSUCCESSFUL = 'unsuccessful'   # unsuccessful  --> /unsuccessful/
SUBMISSION = 'submission'       # submission    --> /submission/


def __create_URL(uri):
    return '/' + uri + '/'


@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect(url_for(LOGIN), code=302)  # because 302 is code for redirection


@app.route(__create_URL(LOGIN), methods=['GET', 'POST'])
def login():
    return render_template('index.html', OTP=OTP)


@app.route(__create_URL(OTP), methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        return render_template('otp.html', DASS21=DASS21)
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(DASS21), methods=['GET', 'POST'])
def dass21():
    if request.method == 'POST':
        return render_template('dass21.html', SUBMISSION=SUBMISSION)
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(SUBMISSION), methods=['GET', 'POST'])
def submission():
    if request.method == 'POST':
        try:
            recipient = 'scc.pec.offcial@gmail.com'
            score_set = backend.calc_score(request=request)
            comments = request.form.get('comments')
            mailing.mailScore(recipient=recipient, score_set=score_set, comments=comments, subject='Score of Student')
            return redirect(url_for('suc_submission'), code=307)        # error code 307 will use the method originallly used for the route which calls redirect
        except Exception as exception:
            return redirect(url_for('unsuc_submission'), code=307)
    else:
        redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(SUCCESSFUL), methods=['GET', 'POST'])
def suc_submission():
    if request.method == 'POST':
        return render_template('suc_submission.html')
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route(__create_URL(UNSUCCESSFUL), methods=['GET', 'POST'])
def unsuc_submission():
    if request.method == 'POST':
        return render_template('unsuc_submission.html')
    else:
        return redirect(url_for(LOGIN), code=302)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
