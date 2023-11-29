#!/usr/bin/env python

import os
import sys
import json
import base64
import requests
import dotenv
from db_utils import _add_professor

ACCESS_TOKEN_URL = "https://api.princeton.edu:443/token"
BASE_URL = "https://api.princeton.edu:443/active-directory/1.0.5"

ENDPOINT = "/members/full"

# Specific to Dondero:
# dotenv.load_dotenv()
# CONSUMER_KEY = os.environ['CONSUMER_KEY']
# CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
CONSUMER_KEY = "KPYMe2FTDdpk9Lo3Q0FLWPWCjwsa"
CONSUMER_SECRET = "ONBGvpgskS6EKutumvlTf_kh56Ua"


def get_cs_professors():
    if len(sys.argv) != 1:
        print("usage: %s" % sys.argv[0], file=sys.stderr)
        sys.exit(1)

    # Use the CONSUMER_KEY and CONSUMER_SECRET to get an access token.

    auth_header = CONSUMER_KEY + ":" + CONSUMER_SECRET
    auth_header = bytes(auth_header, "utf-8")
    auth_header = base64.b64encode(auth_header)
    auth_header = auth_header.decode("utf-8")
    auth_header = "Basic " + auth_header
    response = requests.post(
        ACCESS_TOKEN_URL,
        data={"grant_type": "client_credentials"},
        headers={"Authorization": auth_header},
    )
    response_json_doc = json.loads(response.text)
    access_token = response_json_doc["access_token"]

    # Use the access token to get the data.

    auth_header = "Bearer " + access_token
    print("Access token:", access_token)
    data_url = BASE_URL + ENDPOINT + "?group=Department%2025500%20Faculty"

    response = requests.get(data_url, headers={"Authorization": auth_header})
    response_json_doc = json.loads(response.text)

    # Pretty-print the data.

    return response_json_doc


if __name__ == "__main__":
    jsonProfessors = get_cs_professors()
    for prof in jsonProfessors:
        print(prof['full_name'])

