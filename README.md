# Email Automation Scripts

Scripts for email forwarding and IMAP/SMTP operations.
Detect emails being received to a specific folder and automatically forwards it to a recipient.

## Scripts

- **auto_forward_no_editing.py** - Email forwarding script as is - Pushed
- **forwardv2.py** - Email forwarding script (version 2)
- **forwardv3.py** - Email forwarding script (version 3)
- **forwardv4.py** - Email forwarding script (version 4)
- **test_connection.py** - IMAP connection and email marking utility - Pushed

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
