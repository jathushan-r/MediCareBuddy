from twilio.rest import Client
import re
import random

account_sid = 'ACbe7347deb5dc4fce89ede5304c6dd06c'
auth_token = 'b00cfc97492e78469d93bad7f98e86df'
client = Client(account_sid, auth_token)

def sendSMS(phone):
    otp = generate_otp()
    message = client.messages.create(
        from_= '+16313434034',
        body = f"Your OTP is {otp}",
        to= f"{phone}"
    )

    print(message.sid)
    return otp

# Function to generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))


def convert_to_desired_format(phone_number):
    # Remove any non-digit characters from the phone number
    phone_number = re.sub(r'\D', '', phone_number)

    # Check if the phone number starts with '0' (local format)
    if phone_number.startswith('0'):
        # Remove the leading '0' and add '+94' to the beginning
        phone_number = '+94' + phone_number[1:]
    elif phone_number.startswith('94'):
        phone_number = '+' + phone_number
    return phone_number
def convert_to_desired_format1(phone_number):
    # Remove any non-digit characters from the phone number
    phone_number = re.sub(r'\D', '', phone_number)

    # Check if the phone number starts with '0' (local format)
    if phone_number.startswith('0'):
        # Remove the leading '0' and add '+94' to the beginning
        phone_number = phone_number[1:]
    elif phone_number.startswith('94'):
        phone_number =phone_number[2:]
    return phone_number



# otp = sendSMS("+94712845669")
# print(otp)
# -------------------------------------------------------Response------------------------------------------------------------------------------

# 201 - CREATED - The request was successful. We created a new resource and the response body contains the representation.
# {
#   "body": "Sent from your Twilio trial account - your OTP is 890765",
#   "num_segments": "1",
#   "direction": "outbound-api",
#   "from": "+16313434034",
#   "date_updated": "Sun, 29 Oct 2023 11:03:00 +0000",
#   "price": null,
#   "error_message": null,
#   "uri": "/2010-04-01/Accounts/ACbe7347deb5dc4fce89ede5304c6dd06c/Messages/SM164ebb26172ca839624b84a249511bef.json",
#   "account_sid": "ACbe7347deb5dc4fce89ede5304c6dd06c",
#   "num_media": "0",
#   "to": "+94712845669",
#   "date_created": "Sun, 29 Oct 2023 11:03:00 +0000",
#   "status": "queued",
#   "sid": "SM164ebb26172ca839624b84a249511bef",
#   "date_sent": null,
#   "messaging_service_sid": null,
#   "error_code": null,
#   "price_unit": "USD",
#   "api_version": "2010-04-01",
#   "subresource_uris": {
#     "media": "/2010-04-01/Accounts/ACbe7347deb5dc4fce89ede5304c6dd06c/Messages/SM164ebb26172ca839624b84a249511bef/Media.json"
#   }
# }

# --------------------------------------------------------------------------------------------------------------------------------  