import smtplib
import ssl
import variables

def SendMail(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        variables.smtp_server, variables.port, context=context
    ) as server:
        server.login(variables.sender_email, variables.password)
        server.sendmail(variables.sender_email, variables.receiver_email, message)