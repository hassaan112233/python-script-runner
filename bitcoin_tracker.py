import os
import requests
from twilio.rest import Client

# Load Twilio credentials from environment variables
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

# Twilio WhatsApp Sandbox Details
twilio_sandbox_number = 'whatsapp:+14155238886'
recipient_number = 'whatsapp:+971562276330'

# Initialize Client
if twilio_account_sid and twilio_auth_token:
    client = Client(twilio_account_sid, twilio_auth_token)
else:
    print("Error: Twilio credentials not found. Make sure TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are set as environment variables.")

def get_current_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

def get_previous_day_price():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {'vs_currency': 'usd', 'days': '1'}
    response = requests.get(url, params=params)
    data = response.json()
    previous_day_price = data['prices'][0][1]
    return previous_day_price

def send_notification(current_price, previous_day_price):
    try:
        message = client.messages.create(
            body=f'Bitcoin price has dropped more than 3% in the last 24 hours.\n'
                 f'Current price: ${current_price} USD\nPrevious day\'s price: ${previous_day_price} USD',
            from_=twilio_sandbox_number,
            to=recipient_number
        )
        print(f"Message sent with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

def check_price():
    current_price = get_current_price()
    previous_day_price = get_previous_day_price()
    
    print(f"Current Price: ${current_price} USD")
    print(f"Previous Day's Price: ${previous_day_price} USD")
    
    price_change_percentage = ((previous_day_price - current_price) / previous_day_price) * 100
    
    if price_change_percentage > 1:
        send_notification(current_price, previous_day_price)
    else:
        print("Price drop is less than 1%. No notification sent.")

# Run the script once
check_price()
