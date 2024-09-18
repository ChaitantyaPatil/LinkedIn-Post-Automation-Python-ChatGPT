import requests
from datetime import datetime
from Oauth import auth, headers
import pytgpt.phind as phind

credentials = 'credentials.json'
access_token = auth(credentials) # Authenticate the API
headers = headers(access_token) # Make the headers to attach to the API call.

def user_info(headers):
    '''
    Get user information from Linkedin
    '''
    response = requests.get('https://api.linkedin.com/v2/userinfo', headers = headers)
    user_info = response.json()
    return user_info

# Get user id to make a UGC post
user_info = user_info(headers)
urn = user_info['sub']

# UGC will replace shares over time.
api_url = 'https://api.linkedin.com/v2/ugcPosts'
author = f'urn:li:person:{urn}'

bot = phind.PHIND()
print("-- Creating Post --")
message = bot.chat('engaging LinkedIn post about the technologies in 100 word')
#print(message)

link = 'https://developer.linkedin.com/'
today = datetime.now().strftime("%Y-%m-%d")
#link_text = f"Daily Tech Insights - {today}"

post_data = {
    "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": message
                        },
                        "originalUrl": link,
                        #"title": {
                        #   "text": link_text
                        # }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

if __name__ == '__main__':
    r = requests.post(api_url, headers=headers, json=post_data)
    if r.status_code in [200, 201]:
        print("Post successful!")
    else:
        print(f"Failed to post. Status Code: {r.status_code}")
    
    # Print the response body to inspect further details
    print("Response JSON:", r.json())