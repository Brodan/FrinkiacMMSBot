import schedule
import requests
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Your Account SID from www.twilio.com/console
auth_token  = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'  # Your Auth Token from www.twilio.com/console
client = TwilioRestClient(account_sid, auth_token)

def get_quote():
    r = requests.get("https://frinkiac.com/api/random")
    # Check if our request had a valid response.
    if r.status_code == 200:
        json = r.json()
        # Extract the episode number and timestamp from the API response
        # and convert them both to strings.
        timestamp, episode, _ = map(str, json["Frame"].values())

        image_url = "https://frinkiac.com/meme/" + episode + "/" + timestamp
        # Combine each line of subtitles into one string.
        caption = "\n".join([subtitle["Content"] for subtitle in json["Subtitles"]])
        return image_url, caption

def send_MMS():
    media, body = get_quote()
    try:
        message = client.messages.create(
            body=body,
            media_url=media,
            to="+12345678901",    # Replace with your phone number
            from_="+12345678901") # Replace with your Twilio number
        print("Message sent!")
    # If an error occurs, print it out.
    except TwilioRestException as e:
        print(e)

schedule.every().day.at("12:00").do(send_MMS)

while True:
    schedule.run_pending()
