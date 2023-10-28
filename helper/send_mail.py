import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail:
    def __init__(self, email, password):
        self.smtp_port = 587
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_username = email
        self.smtp_password = password
        self.smtp_conn = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.smtp_conn.starttls()
        self.smtp_conn.login(self.smtp_username, self.smtp_password)

    def send_mail(self, to_send_list, mail_subject, mail_body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = ', '.join(to_send_list)
        msg['Subject'] = mail_subject
        msg.attach(MIMEText(mail_body, 'plain'))

        self.smtp_conn.sendmail(self.smtp_username, to_send_list, msg.as_string())
        self.smtp_conn.quit()
