import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PORT = 465
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'scc.pec.offcial@gmail.com'
PASSWORD = 'scc-website'      # should be encrypted or loaded from a file using template


def mail(recipient_email, message=None):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())


def mailOTP(recipient_email, otp):

    message = MIMEMultipart('alternative')
    message['Subject'] = 'OTP - SCC Website'
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email

    text = """\
    Hi,
    Your OTP is {otp}"""
    html = """\
    <html>
        <body>
            <p>Hi,<br/>
            Your OTP is <strong>{otp}</strong>.
            </p>
        </body>
    </html>"""

    text = text.format(otp=otp)
    text = text.format(otp=otp)
    html = html.format(otp=otp)
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')
    message.attach(text_part)
    message.attach(html_part)

    mail(recipient_email, message)


def mailScore(recipient, score_set=None, comments=None,  subject='Score of Student'):
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = recipient

    text = """\
        Hi,
        The score of student {name} is:-
            1. Stress Score: {stress}
            2. Anxiety Score: {anxiety}
            3. Depression: {depression}
            
        Student Details:
        Name: {name}
        SID: {sid}
        Contact: {contact}
        Email: {email}
        
        Additional Comments by Student: {comments}
        """
    html = """\
        <html>
            <body>
                <p>Hi,<br/>
                The score of student {name} is:- <br/>
                    1. Stress Score: <strong>{stress}</strong> <br/>
                    2. Anxiety Score: <strong>{anxiety}</strong> <br/>
                    3. Depression: <strong>{depression}</strong> <br/>
                    <br/>
                Student Details: <br/>
                Name: <strong>{name}</strong> <br/>
                SID: <strong>{sid}</strong> <br/>
                Contact: <strong>{contact}</strong> <br/>
                Email: <strong>{email}</strong> <br/>
                <br/>
                Additional Comments by Student: {comments}<br/>
                </p>
            </body>
        </html>"""

    if comments is None:
        comments = 'NA'

    # TODO add the code segment to replace the student details
    text = text.format(stress=score_set['stress'], anxiety=score_set['anxiety'], depression=score_set['depression'],
                       name='Name', sid='SID', contact='Contact', email='Email', comments=comments)
    html = html.format(stress=score_set['stress'], anxiety=score_set['anxiety'], depression=score_set['depression'],
                       name='Name', sid='SID', contact='Contact', email='Email', comments=comments)
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')
    message.attach(text_part)
    message.attach(html_part)

    mail(recipient, message)
