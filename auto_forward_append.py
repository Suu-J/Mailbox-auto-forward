'''
I've commented out the extra append at the bottom of the email body, the special symbols are for identification

Imports for mail text processing
Email configuration
Connecting to Outlook's IMAP server
    Iterating through each unread email
        Create a forwarding message
        Extract text/plain content from the email
        Extract the sender's email address
        Format the email address as desired
        Append formatted sender's email address to the body
        Set the email body as the body of the forwarded message
        Connect to SMTP server and send the email
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
# The folder to peek into
mail.select("instant_forward")

# searching for unread emails, mail.search returns a tuple
result, data = mail.search(None, "(UNSEEN)")

if result == "OK":
    for num in data[0].split():
        result, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # [ CHECK ] ->  if FROM can hold sender email instead of login account ( should be possible )
        forward_msg = MIMEMultipart()
        forward_msg["From"] = outlook_username
        forward_msg["To"] = forward_to
        forward_msg["Subject"] = msg["Subject"]

        email_body = "" # build this variable progressively
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body += part.get_payload(decode=True).decode()

        sender_email = msg.get("From")
        
        # extracting the address only
        sender_name, sender_address = email.utils.parseaddr(sender_email)

        formatted_sender_email = f"Sender's Email Address &#^[{sender_address}]"

        email_body += f"\n\n{formatted_sender_email}"

        # old append
        # email_body += f"\n\n&#^Sender's Email Address -> [{sender_email}]"
        print(sender_email) # test console logging

        forward_msg.attach(MIMEText(email_body, "plain"))

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()  # Securing the connection over transit
            server.login(outlook_username, outlook_password)
            server.sendmail(outlook_username, forward_to, forward_msg.as_string())
    print("Forwarded all unread emails.")

mail.close()
mail.logout()
