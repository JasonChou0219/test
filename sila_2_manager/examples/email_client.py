import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(attachment):
    sender_email = "lukas.bromig@gmail.com"
    receiver_email = "lukas.bromig@tum.de"
    password = 'c5hl6683w'  ##input("Type your password and press enter:")

    message = MIMEMultipart("alternative")
    message["Subject"] = "BIOLAGO HACKATHON pump calibration results"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    These are the latest pump calibration results!
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(attachment)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
