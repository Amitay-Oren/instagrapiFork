import imaplib
import email
import email
import re


# Function to connect to the email server
def connect_to_email(email_address, password):
    email_address: str
    password: str
    mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Modify this if not using Gmail
    mail.login(email_address, password)
    mail.select("inbox")  # Connect to the inbox
    return mail


# Function to search for the latest Instagram 2FA code
def get_instagram_code(mail):
    result, data = mail.search(
        None, '(FROM "security@mail.instagram.com")'
    )  # Update the sender if needed
    if result == "OK":
        # Get the latest email id
        latest_email_id = data[0].split()[-1]
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        # Parse the email content
        msg = email.message_from_bytes(raw_email)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload()
                    if isinstance(payload, bytes):
                        body = payload.decode()
                    else:
                        body = payload
                    # Regex to find the 2FA code
                    match = re.search(r"\d{6}", str(body))
                    if match:
                        return match.group(0)
        else:
            payload = msg.get_payload()
            if isinstance(payload, bytes):
                body = payload.decode()
            else:
                body = payload
            match = re.search(r"\d{6}", str(body))
            if match:
                return match.group(0)
    return None
