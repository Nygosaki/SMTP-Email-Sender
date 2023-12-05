import dotenv
import os
import smtplib, ssl
import re
import dns.resolver
from email.message import EmailMessage

try:
    dotenv.load_dotenv()
    smtpSever = os.getenv("SMTPSERVER")
    smtpSeverPort = os.getenv("SMTPSERVERPORT")
    smtpServerUser = os.getenv("SMTPSERVERUSER")
    smtpServerToken = os.getenv("SMTPSERVERTOKEN")
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
    replyto = os.getenv("REPLYTO")
except:
    print("Per-Email variables have not been defined in the .env file. Presets have not been loaded.")
    sender = input("What is the sender email address?\n>")
    senderName = input("What is the sender's name?\n>")
    reciever = input("Who is the recipient? If there are multiple, seperate them with ;. \nEx: admin@example.com;user@example2.com\n>")
    subject = input("What is the subject of the email?\n>")
    content = input("What would you like the body of the email to contain?\n>")
    replyto = input("What email adress would you like email clients to automatically reply to when a user clicks 'reply' to the email?\n>")

em = EmailMessage()
em['From'] = f"{senderName} <{sender}>"
em['To'] = reciever
em['Subject'] = subject
em['Reply-To'] = replyto
em.set_content(content)


domain = re.split("@", sender)[1]
print ("Testing domain", domain, "for DMARC record...")
try:
    test_dmarc = dns.resolver.resolve('_dmarc.' + domain , 'TXT')
    for dns_data in test_dmarc:
        if 'DMARC1' in str(dns_data):
            print ("DMARC record found :",dns_data)
            dmarc_sort = dict()
            try:
                dmarc_sort["p"] = re.findall('p=(.*?)[; \n]', str(dns_data))[0]
                if dmarc_sort["p"].lower() == "quarantine":
                    print("Warning: Your email will go to spam or be filtered")
            except:
                dmarc_sort["p"] = "null"
                print("There seems to be something wrong with the `p` value")
            try:
                dmarc_sort["sp"] = re.findall('sp=(.*?)[; \n]', str(dns_data))[0]
                if dmarc_sort["sp"] != dmarc_sort["p"]:
                    print(f"the `sp` record is not the same as `p`. `sp: {dmarc_sort['sp']}")
            except:
                dmarc_sort["sp"] = dmarc_sort["p"]
            try:
                dmarc_sort["pct"] = re.findall('pct=(.*?)[; \n]', str(dns_data))[0]
                if dmarc_sort["p"].lower() == "reject" and str(dmarc_sort["pct"]) == "100":
                    print("The email will be rejected")
                    exit()
                else:
                    print(f"There is a {dmarc_sort['pct']}% chance that the `p` policy will be enforced")
            except:
                dmarc_sort["pct"] = "100"
                if dmarc_sort["p"].lower() == "reject":
                    print("The email will be rejected")
                    exit()
            try:
                dmarc_sort["fo"] = re.findall('fo=(.*?)[; \n]', str(dns_data))[0]
                if "0" in dmarc_sort["fo"]:
                    print("fo=0: Generate a DMARC failure report if all underlying authentication mechanisms (SPF and DKIM) fail to produce an aligned “pass” result.")
                if "1" in dmarc_sort["fo"]:
                    print("fo=1: Generate a DMARC failure report if any underlying authentication mechanism (SPF or DKIM) produced something other than an aligned “pass” result.")
                if "d" in dmarc_sort["fo"]:
                    print("fo=d: Generate a DKIM failure report if the message had a signature that failed evaluation, regardless of its alignmen")
                if "s" in dmarc_sort["fo"]:
                    print("fo=s: Generate an SPF failure report if the message failed SPF evaluation, regardless of its alignment.")
            except:
                dmarc_sort["fo"] = "0"
                print("fo=0: Generate a DMARC failure report if all underlying authentication mechanisms (SPF and DKIM) fail to produce an aligned “pass” result. (Default)")
            try:
                dmarc_sort["ruf"] = re.findall('ruf=(.*?)[; \n]', str(dns_data))[0]
                print(f"ruf: {dmarc_sort['ruf']}")
            except:
                dmarc_sort["ruf"] = "none"
            try:
                dmarc_sort["rua"] = re.findall('rua=(.*?)[; \n]', str(dns_data))[0]
                print(f"rua: {dmarc_sort['rua']}")
            except:
                dmarc_sort["rua"] = "none"

            print(dmarc_sort)
except:
    print ("DMARC record not found.")
    pass

if input("Considering this information, would you still like to continue? (Y/N)\n>").lower() == "n":
    exit()

try:
    context = ssl.create_default_context()
    with smtplib.SMTP(smtpSever, smtpSeverPort) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(smtpServerUser, smtpServerToken)
        server.send_message(em, sender, reciever)
    print('Email sent!')
except Exception as exception:
    print("Error: %s!\n\n" % exception)
