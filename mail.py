import re
import smtplib
import ssl
import variables

def mail_check(mail):
    pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\\.[A-Z|a-z]{2,})+"
    return re.match(pattern, mail) is not None

def email_validity():
    sender_boolean = mail_check(variables.sender_email)
    receiver_boolean = mail_check(variables.receiver_email)

    if not sender_boolean and not receiver_boolean:
        print("Sender email and receiver email are incorrect.")
    elif not sender_boolean:
        print("Sender email is incorrect.")
    elif not receiver_boolean:
        print("Receiver email is incorrect.")
    else:
        return True
    
def send_mail(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        variables.smtp_server, variables.port, context=context
    ) as server:
        server.login(variables.sender_email, variables.password)
        server.sendmail(variables.sender_email, variables.receiver_email, message)

validity_check = email_validity()

send_check = False