from telethon import TelegramClient, events
import re
import webbrowser
import time

# Your API_ID and API_HASH (replace with actual values)
API_ID = '23289938'  # Replace with your API_ID
API_HASH = 'e700b97900cb151dd394640b5cc93ffb'  # Replace with your API_HASH

# The name of the session file, it will save your login session
SESSION_NAME = 'referral_code_reader_' + str(time.time())  # Add a timestamp or unique identifier


# Create the Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Channel's link or username (replace with the actual channel's link or username)
CHANNEL_LINK = 'https://t.me/BonusCodesStake'
# CHANNEL_LINK = 'https://t.me/Demo123456789010'  # Use the channel username or full link

# Function to extract referral codes (modify regex based on your needs)
def extract_referral_code(message_text):
    """ Extracts the referral code from the message with or without 'Code:' """
    # Step 1: Try to match "Code: ABC123"
    match = re.findall(r'(?i)\bcode[:\s]*([a-zA-Z0-9_-]+)\b', message_text)
    
    # Step 2: If no "Code:" is found, try to find a standalone code
    if not match:
        # Extract single words that could be a referral code (avoid extracting entire sentences)
        # Here, we're looking for standalone codes in the message.
        match = re.findall(r'\b([a-zA-Z0-9_-]{6,20})\b', message_text)  # Length limit 6-20 characters

    return match[0] if match else None  # Return only the first match (if multiple codes exist)

# Function to listen for new messages in real-time
@client.on(events.NewMessage(chats=CHANNEL_LINK))
async def new_message_listener(event):
    message = event.message
    if message.text:
    # Extract the referral code from the message
        latest_referral_code = extract_referral_code(message.text)
    if latest_referral_code:
        print(f"✅ Found referral code: {latest_referral_code}")
        
        # Save the referral code in a file
        with open("referral_codes.txt", "a") as file:
            file.write(f"{latest_referral_code}\n")
        
        # Print the referral link with the code
        url = f"https://stake.bet/settings/offers?type=drop&code={latest_referral_code}&currency=btc&modal=redeemBonus"
        print(url)
        
        # Open the link in the default browser
        webbrowser.open(url)

# Run the client and listen for new messages
with client:
    print(f"👂 Listening for referral codes in channel '{CHANNEL_LINK}'...")
    client.run_until_disconnected()  # Keep running until disconnected
