from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email_with_invoice(to_email, student_name, invoice_path):
    """Send an email with the invoice attached."""
    from_email = EMAIL_USER
    app_password = EMAIL_PASSWORD
    subject = f"Invoice for {student_name}"
    body = f"Dear Parent,\n\nPlease find attached the invoice for {student_name}.\n\nThank you."

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(invoice_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(invoice_path)}")
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, app_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

    print(f"Invoice sent to {to_email} for {student_name}.")
