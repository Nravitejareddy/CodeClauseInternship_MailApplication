import smtplib
from email.message import EmailMessage
from datetime import datetime
from database import cursor, conn

def send_email(user_id, to, subject, body):
    """Send email using SMTP configuration from DB"""
    cursor.execute(
        "SELECT email, server, port, app_password FROM smtp_settings WHERE user_id=?",
        (user_id,)
    )
    data = cursor.fetchone()
    if not data:
        return False, "SMTP not configured"

    sender, server, port, password = data

    try:
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(server, port) as s:
            s.starttls()
            s.login(sender, password)
            s.send_message(msg)

        # Store sent mail in DB
        cursor.execute(
            "INSERT INTO sent_mails VALUES (NULL,?,?,?,?,?,?)",
            (user_id, to, subject, body, datetime.now().strftime("%Y-%m-%d %H:%M"), "Sent")
        )
        conn.commit()
        return True, "Mail Sent Successfully"

    except Exception as e:
        return False, f"Failed to send mail: {str(e)}"
