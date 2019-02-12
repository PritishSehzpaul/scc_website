from flask import Flask, render_template, redirect, url_for, request

app = Flask('scc')

###  routes for webpages
LOGIN = 'login'                 # login --> /login/
OTP = 'otp'                     # otp --> /otp/
DASS21 = 'dass21'               # dass21 --> /dass21/
SUBMISSION = 'submission'       # submission --> /submission/


@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect(url_for(LOGIN), code=302)     # because 302 is code for redirection


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('index.html')


@app.route('/otp/', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        return render_template('otp.html')
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route('/dass21/', methods=['GET', 'POST'])
def dass21():
    if request.method == 'POST':
        return render_template('dass21.html')
    else:
        return redirect(url_for(LOGIN), code=302)


@app.route('/submission/', methods=['GET', 'POST'])
def submission():
    if request.method == 'POST':
        return render_template('submission.html')
    else:
        return redirect(url_for(LOGIN), code=302)




if __name__ == '__main__':
    app.run(debug=True)
