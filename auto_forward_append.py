import imaplib
import email
import smtplib
# Imports for mail text processing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
outlook_server = "outlook.office365.com"
outlook_username = ""
outlook_password = ""
forward_to = ""

# Connecting to Outlook's IMAP server
mail = imaplib.IMAP4_SSL(outlook_server)
mail.login(outlook_username, outlook_password)
# The folder to peek into
mail.select("autotest")

# Searching for unread emails, mail.search returns a tuple
result, data = mail.search(None, "(UNSEEN)")

if result == "OK":
    # Iterating through each unread email
    for num in data[0].split():
        result, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Create a forwarding message
        # [ CHECK ] ->  if FROM can hold sender email instead of login account ( should be possible )
        forward_msg = MIMEMultipart()
        forward_msg["From"] = outlook_username
        forward_msg["To"] = forward_to
        forward_msg["Subject"] = msg["Subject"]

        # Extract text/plain content from the email
        email_body = "" # build this variable progressively
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body += part.get_payload(decode=True).decode()

        # Extract the sender's email address
        sender_email = msg.get("From")
        
        # extracting the address only
        sender_name, sender_address = email.utils.parseaddr(sender_email)

        # Format the email address as desired
        formatted_sender_email = f"Sender's Email Address &#^[{sender_address}]"

        # Append formatted sender's email address to the body
        email_body += f"\n\n{formatted_sender_email}"

        # old append
        # email_body += f"\n\n&#^Sender's Email Address -> [{sender_email}]"
        print(sender_email) # test console logging

        # Set the email body as the body of the forwarded message
        forward_msg.attach(MIMEText(email_body, "plain"))

        # Connect to SMTP server and send the email
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()  # Securing the connection
            server.login(outlook_username, outlook_password)
            server.sendmail(outlook_username, forward_to, forward_msg.as_string())
    print("Forwarded all unread emails.")

mail.close()
mail.logout()
