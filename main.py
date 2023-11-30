import dotenv
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

try:
    dotenv.load_dotenv()
    smtpSever = os.getenv("SMTPSERVER")
    smtpSeverPort = os.getenv("SMTPSERVERPORT")
    smtpServerUser = os.getenv("SMTPSERVERUSER")
    smtpServerToken = os.getenv("SMTPSERVERTOKEN")
    sender = os.getenv("SENDER")
    senderName = os.getenv("SENDERNAME")
    reciever = os.getenv("RECIEVER")
except:
    print("A .env file was not found. Presets have not been loaded.")
    smtpSever = input("What is your origin SMTP serve?\n>")
    smtpSeverPort = input("What is the port of the origin SMTP server?\n>")
    smtpServerUser = input("What is the user authentication for the SMTP server?\n>")
    smtpServerToken = input("What is the password authentication for SMTP server?\n>")

try:
    sender = os.getenv("SENDER")
    senderName = os.getenv("SENDERNAME")
    reciever = os.getenv("RECIEVER")
    subject = os.getenv("SUBJECT")
    content = os.getenv("CONTENT")
except:
    print("Per-Email variables have not been defined in the .env file. Presets have not been loaded.")
    sender = input("What is the sender email address?\n>")
    senderName = input("What is the sender's name?\n>")
    reciever = input("Who is the recipient? If there are multiple, seperate them with ;. \nEx: admin@example.com;user@example2.com\n>")
    subject = input("What is the subject of the email?\n>")
    content = input("What would you like the body of the email to contain?\n>")

message = f"""From: {senderName} <{sender}>
Subject: {subject}

{content}
"""

try:
    context = ssl.create_default_context()
    with smtplib.SMTP(smtpSever, smtpSeverPort) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(smtpServerUser, smtpServerToken)
        server.sendmail(sender, reciever, message)
    print('Email sent!')
except Exception as exception:
    print("Error: %s!\n\n" % exception)
