import requests
import base64

CONSUMER_KEY = "KPYMe2FTDdpk9Lo3Q0FLWPWCjwsa"
CONSUMER_SECRET = "ONBGvpgskS6EKutumvlTf_kh56Ua"

req = requests.get(
    url='https://api.princeton.edu:443/active-directory/1.0.2/members/full',
    params="Department 25500 Faculty",
    headers={
        "Authorization": "Basic " + base64.b64encode(bytes(CONSUMER_KEY + ":" + CONSUMER_SECRET, "utf-8")).decode("utf-8")
    },
)

print(req.text)