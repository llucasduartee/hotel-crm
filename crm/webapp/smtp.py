import smtplib
from email.mime.text import MIMEText

def send_email_async(subject, message, from_email, recipient_list):
    # Create a MIME text object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(recipient_list)

    # Connect to the SMTP server with TLS support
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Enable TLS
    server.login('lucasduartedsvp@gmail.com', 'ktyfdtfjtpkiicdt')  # Authenticate with your Gmail account
    server.sendmail(from_email, recipient_list, msg.as_string())
    server.quit()

    return 'Email sent to {}.'.format(recipient_list)