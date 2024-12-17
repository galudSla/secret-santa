# import smtplib
import random
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

import os
import json
from openai import OpenAI


SCOPES = ['https://www.googleapis.com/auth/gmail.send']
# app_email = 'xxxxxxxxxxx@gmail.com'
# app_email = os.getenv(app_email)

def selection_excluding(lst, exception):
    possible_choices = [v for v in lst if v != exception]
    return random.choice(possible_choices)


def santa_pick(participants):
    choices = list(participants.keys())
    for key in participants.keys():
        temp = selection_excluding(choices, key)
        participants[key]['gift_to'] = temp
        choices.remove(temp)
    return participants


def chatgpt_recommendation(participants):
    for key in participants.keys():
        temp = chatgpt_call(participants[key]['gift_prompt'])
        participants[key]['gift_list'] = temp
    return participants


def send_emails(participants):
    for key in participants.keys():
        name = key
        email = participants[key]['email']
        gift_to = participants[key]['gift_to']
        gift_list = participants[gift_to]['gift_list']
        gmail_send_message(name, email, gift_to, gift_list)


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    print("Authentication successful. Token saved as 'token.json'.")


def gmail_send_message(name, recipient, gifts_to, gifts):
    body = f'''Hello {name}!

The holiday season is here, and it's time for Secret Santa! You'll be gifting something special to {gifts_to}.

Here are some gift ideas to get you started:
{gifts}

Take your time, think of something thoughtful, and make their holidays brighter!

Cheers,
Your Secret Santa team.
'''

    ## change with gmail_send is that the token is saved as 'credentials' environment variable
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # else:
    #     raise FileNotFoundError("Token file not found. Please authenticate first.")

    creds = None  
    if 'token' in os.environ:
        token = json.loads(os.getenv('token'))
        creds = Credentials.from_authorized_user_info(token, SCOPES)
    else:
        raise FileNotFoundError("Token file not found. Please authenticate first.")

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(body)

        message["To"] = recipient
        message["From"] = app_email
        message["Subject"] = "Secret Santa"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message




def chatgpt_call(user_info):
    if user_info == '':
        user_info = 'No info has been provided. Make a generic recommendation.'

    client = OpenAI(
        # api_key=os.getenv('OPENAI_API_KEY'),
    )

    completion  = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "Provide gift recommendations based on the given information about a person for a Secret Santa generator application. Focus only on the recommendations and format them in a list.\n\n# Additional Details\n\n- The information you will receive may include hobbies, interests, and preferences.\n- Avoid any commentary or additional information in your response.\n\n# Output Format\n\n- Provide recommendations in a simple list format, ensuring clarity and relevance to the provided information.\n\n# Notes\n\n- Make sure recommendations are varied and appropriate to the individual based on available data.\n- Limit your recommendations to a reasonable number that can easily be reviewed at a glance."
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": user_info
            }
        ]
        }
    ],
    response_format={
        "type": "text"
    },
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return completion.choices[0].message.content


### SMTP send legacy deprecated
# def mail(name, dest, gift_to):

#     sender_email = "xxxxxxxxxx@gmail.com"
#     sender_password = "xxxxxxxxxxxxxx"



#     message = f"""From: {sender_email}
# To: {dest}
# Subject: Your Secret Santa Match Is Here!

# Hi {name},

# The holiday season is here, and it's time for some Secret Santa fun!

# You'll be gifting something special to {gift_to}!

# Take your time, think of something thoughtful, and help make their holidays a little brighter.

# Cheers,
# Your Secret Santa Team
# """

#     try:
#         s = smtplib.SMTP('smtp.gmail.com', 587)
#         s.starttls()
#         s.login(sender_email, sender_password)
#         s.sendmail(sender_email, dest, message)
#         print(f"Email sent successfully to {name}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         s.quit()


if __name__ == "__main__":
    authenticate()