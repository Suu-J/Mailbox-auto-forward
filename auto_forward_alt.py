'''
Docstring for email_automation.auto_forward_alt

Second version, I removed some functionalities, i used this parallelly

Add email configs,
connecto outlook's imap server
serach all unread emails
go through each unread email
build a forward message body
attach og email to forward body
connect to smtp and send email

'''

import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

outlook_server = "outlook.office365.com"
outlook_username = ""
outlook_password = ""
forward_to = ""

mail = imaplib.IMAP4_SSL(outlook_server)
mail.login(outlook_username, outlook_password)
mail.select("inbox")

result, data = mail.search(None, "(UNSEEN)")

if result == "OK":
    for num in data[0].split():
        result, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        forward_msg = MIMEMultipart()
        forward_msg["From"] = outlook_username
        forward_msg["To"] = forward_to
        forward_msg["Subject"] = msg["Subject"]

        forward_msg.attach(MIMEText("Forwarded message attached.", "plain"))
        forward_msg.attach(MIMEText(msg.as_string(), "rfc822"))

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()  
            server.login(outlook_username, outlook_password)
            server.sendmail(outlook_username, forward_to, forward_msg.as_string())
    print("Forwarded all unread emails.")

mail.close()
mail.logout()
