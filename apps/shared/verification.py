from random import randint

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from root.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_SID

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
verify = client.verify.services(TWILIO_VERIFY_SERVICE_SID)

fake_code = None


def send(phone, fake=False):
    if fake:
        global fake_code
        fake_code = randint(1000, 9999)
        print(fake_code)
        return
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code, fake=False):
    if fake:
        global fake_code
        return fake_code == int(code)
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'
