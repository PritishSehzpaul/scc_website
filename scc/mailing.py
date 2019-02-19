import smtplib
import ssl
from config.configuration import Configuration
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO add a check whether the email was received by the client

# initializing config variables
config = Configuration().config
PORT = config['mailing']['port']
SMTP_SERVER = config['mailing']['smtp_server']
SENDER_EMAIL = config['mailing']['sender_email']
PASSWORD = config['mailing']['password']


def mail(recipient_email, message=None):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())


def mailOTP(session, otp):
    recipient_email = session['email']
    recipient_name = session['name']

    message = MIMEMultipart('alternative')
    message['Subject'] = 'OTP - SCC Website'
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email

    text = """\
    Hi {name},
    Your OTP is {otp}"""
    html = """\
    <html>
        <body>
            <p>Hi {name},<br/>
            Your OTP is <strong>{otp}</strong>.
            </p>
        </body>
    </html>"""

    text = text.format(name=recipient_name, otp=otp)
    html = html.format(name=recipient_name, otp=otp)
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')
    message.attach(text_part)
    message.attach(html_part)

    mail(recipient_email, message)


def mailScore(session, recipient, score_set=None, comments=None,  subject='Score of Student'):
    user_email = session['email']
    user_name = session['name']
    user_contact = session['contact']
    user_sid = session['sid']

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = recipient

    text = """\
        Hello Mam,
        The score of student {name} is:-
            1. Stress Score:  {stress}
            2. Anxiety Score: {anxiety}
            3. Depression:    {depression}
            
        Student Details:
        Name:     {name}
        SID:      {sid}
        Contact:  {contact}
        Email Id: {email}
        
        Additional Comments by Student: {comments}
        """
    html = """\
        <html>
            <body>
                <p>Hello Mam,<br/>
                The score of student {name} is:- <br/>
                &nbsp;&nbsp;&nbsp;&nbsp;1. Stress Score: &nbsp;&nbsp;<strong>{stress}</strong> <br/>
                &nbsp;&nbsp;&nbsp;&nbsp;2. Anxiety Score: &nbsp;<strong>{anxiety}</strong> <br/>
                &nbsp;&nbsp;&nbsp;&nbsp;3. Depression: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>{depression}</strong> <br/>
                    <br/>
                Student Details: <br/>
                Name: &nbsp;&nbsp;&nbsp;&nbsp;<strong>{name}</strong> <br/>
                SID: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>{sid}</strong> <br/>
                Contact: &nbsp;<strong>{contact}</strong> <br/>
                Email Id: <strong>{email}</strong> <br/>
                <br/>
                <i>Additional Comments by Student: {comments}</i><br/>
                </p>
            </body>
        </html>"""

    if comments is None:
        comments = 'NA'

    # TODO add the code segment to replace the student details
    text = text.format(stress=score_set['stress'], anxiety=score_set['anxiety'], depression=score_set['depression'],
                       name=user_name, sid=user_sid, contact=user_contact, email=user_email, comments=comments)
    html = html.format(stress=score_set['stress'], anxiety=score_set['anxiety'], depression=score_set['depression'],
                       name=user_name, sid=user_sid, contact=user_contact, email=user_email, comments=comments)
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')
    message.attach(text_part)
    message.attach(html_part)

    mail(recipient, message)
