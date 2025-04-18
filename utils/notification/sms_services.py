from twilio.rest import Client
from core import settings


class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_sms(self, to_phone_number, message_body):
        """
        使用 Twilio API 發送 SMS
        :param to_phone_number: 收件者電話號碼（含國碼，例如：+886912345678）
        :param message_body: 簡訊內容
        :return: Twilio 訊息物件
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to_phone_number
            )
            return {"message_sid": message.sid, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}


send_sms = TwilioService().send_sms


if __name__ == '__main__':
    sms = TwilioService()
    sms.send_sms("+886988795855", "我是來自Joe的測試訊息")
