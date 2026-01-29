# Email Automation Scripts

Scripts for email forwarding and IMAP/SMTP operations.
Detect emails being received to a specific folder and automatically forwards it to a recipient.
Can append more content to the email body as you send.

## Scripts

- **auto_forward_no_editing.py** - Email forwarding script as is
- **auto_forward_alt.py** - alternate of no edit
- **auto_forward_ukw.py** - idk which version - pushed it just in case
- **auto_foward_append.py** - Added the sender email to body
- **test_connection.py** - IMAP connection and email marking utility

## Typical Workflow
1. Connect to IMAP server
2. Retrieve unread emails
3. Process email content
4. Forward via SMTP
5. Mark emails as read

## Dependencies
- imaplib
- smtplib
- email (Python standard library)

## Configuration
Scripts typically require:
- IMAP server credentials
- SMTP server credentials
- Email addresses for forwarding
