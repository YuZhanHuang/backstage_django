from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# 設定 SendGrid API Key
SENDGRID_API_KEY = ""
SENDER_EMAIL = ""  # 必須是已驗證的寄件者
RECIPIENT_EMAIL = ""


def send_email(target_mail, html_content, subject, plain_text_content):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=target_mail,
        subject=subject,
        plain_text_content=plain_text_content,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

