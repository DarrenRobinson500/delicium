from datetime import time, timedelta, datetime
from twilio.rest import Client
from app.models import *

def read_file(text):
    file = open("SECRET_KEYS.txt")
    data = file.readlines()
    file.close()
    for line in data:
        parts = line.strip().split(" ")
        if parts[0] == text:
            return parts[1]


account_sid = read_file("account_sid")
auth_token = read_file("auth_token")
my_twilio_number = read_file("my_twilio_number")
target_number = read_file("target_number")

client = Client(account_sid, auth_token)

def send_sms():
    body = get_birthday_reminders()
    print("Body:", body)
    if body != "":
        print(f"Sending SMS: {body}")
        client.messages.create(body=body, from_=my_twilio_number, to=target_number)

