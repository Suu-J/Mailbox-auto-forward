'''
Docstring for Script email_automation.

I honestly forgot why i made this version

Connect to Outlook's IMAP server
Search for unread emails, mail.search returns a tuple
    Iterate through each unread email
        Create a forwarding message
        Extract text/plain content from the email
        Set the email body as the body of the forwarded message
        Connect to SMTP server and send the email
            
'''

import imaplib
import email
import smtplib
# Imports for mail text processing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

outlook_server = "outlook.office365.com"
outlook_username = ""
outlook_password = ""
forward_to = ""

mail = imaplib.IMAP4_SSL(outlook_server)
mail.login(outlook_username, outlook_password)
# The folder to peek into
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

        email_body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body += part.get_payload(decode=True).decode()

        forward_msg.attach(MIMEText(email_body, "plain"))

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()  # securing the connection
            server.login(outlook_username, outlook_password)
            server.sendmail(outlook_username, forward_to, forward_msg.as_string())
    print("Forwarded all unread emails.")


mail.close()
mail.logout()
