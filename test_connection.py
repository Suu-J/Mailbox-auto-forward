'''
Docstring for Script email_automation.test_connection

you have to give username and password like usual for this,
use the imap library for connecting to outlook's imap server, mail.select i think is folder selection

'''

import imaplib

outlook_server = "outlook.office365.com"
outlook_username = ""
outlook_password = ""

mail = imaplib.IMAP4_SSL(outlook_server)
mail.login(outlook_username, outlook_password)
mail.select("inbox")

result, data = mail.search(None, "(UNSEEN)")

if result == "OK":
    # Gettung the list of unread email IDs
    unread_email_ids = data[0].split()

    # Mark unread emails as read, or else it will always be picked
    for email_id in unread_email_ids:
        mail.store(email_id, "+FLAGS", "\\Seen")
    print(f"Marked {len(unread_email_ids)} unread email(s) as read.")

mail.close()
mail.logout()

