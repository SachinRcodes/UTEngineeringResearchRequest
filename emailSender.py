
import imaplib
import time
from email.message import EmailMessage
import os

# Get credentials from environment variables (or you can hardcode if testing)
# Use Gmail App Password if 2FA is enabled

def send_email(email_subject, email_body, recipient_email):
    # MODIFY THIS
    sender_email_address = os.environ['EMAIL_USER']
    # MODIFY THIS
    sender_email_password = os.environ['EMAIL_PASS']
    
    # Create the email message (a draft)
    email_message = EmailMessage()
    email_message.set_content(email_body)
    email_message['Subject'] = email_subject
    email_message['From'] = sender_email_address
    email_message['To'] = recipient_email

    # Convert the EmailMessage object to bytes
    utf8_email_message = email_message.as_bytes()

    # Save the message to Gmail Drafts via IMAP
    with imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT) as imap_connection:
        print("Logging into mailbox...")
        response_code, login_response = imap_connection.login(sender_email_address, sender_email_password)

        # Append to Drafts folder
        imap_connection.append("[Gmail]/Drafts", '', imaplib.Time2Internaldate(time.time()), utf8_email_message)
        print("Draft saved successfully.")
