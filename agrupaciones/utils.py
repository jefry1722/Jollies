import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


def enviarCorreo(to, subject, message_to_send):
    port = 587
    email = "jolliesapp@gmail.com"
    codigo = env('EMAIL_CODE')
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(message_to_send))
    server = smtplib.SMTP("smtp.gmail.com", port)
    server.starttls()
    server.login(email, codigo)
    server.sendmail(email, [to], message.as_string())
    server.quit()
