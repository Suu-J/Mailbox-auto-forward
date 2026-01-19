import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
outlook_server = "outlook.office365.com"
outlook_username = ""
outlook_password = ""
forward_to = ""

# Connect to Outlook's IMAP server
mail = imaplib.IMAP4_SSL(outlook_server)
mail.login(outlook_username, outlook_password)
mail.select("inbox")

# Search for unread emails
result, data = mail.search(None, "(UNSEEN)")

if result == "OK":
    # Iterate through each unread email
    for num in data[0].split():
        result, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Create a forwarding message
        forward_msg = MIMEMultipart()
        forward_msg["From"] = outlook_username
        forward_msg["To"] = forward_to
        forward_msg["Subject"] = msg["Subject"]

        # Add original email as attachment
        forward_msg.attach(MIMEText("Forwarded message attached.", "plain"))
        forward_msg.attach(MIMEText(msg.as_string(), "rfc822"))

        # Connect to SMTP server and send the email
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(outlook_username, outlook_password)
            server.sendmail(outlook_username, forward_to, forward_msg.as_string())
    print("Forwarded all unread emails.")

# Close the connection to the IMAP server
mail.close()
mail.logout()
