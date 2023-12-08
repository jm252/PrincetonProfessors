#!/usr/bin/env python

import os
import sys
import json
import base64
import requests
import dotenv
from db_utils import add_professor

ACCESS_TOKEN_URL = "https://api.princeton.edu:443/token"
BASE_URL = "https://api.princeton.edu:443/active-directory/1.0.5"

ENDPOINT = "/members/full"

# Specific to Dondero:
# dotenv.load_dotenv()
# CONSUMER_KEY = os.environ['CONSUMER_KEY']
# CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
CONSUMER_KEY = "KPYMe2FTDdpk9Lo3Q0FLWPWCjwsa"
CONSUMER_SECRET = "ONBGvpgskS6EKutumvlTf_kh56Ua"

DEPT_LIST = [
    (22100, "AAS"),
    (28000, "AMS"),
    (22000, "ANT"),
    (20000, "ARC"),
    (20100, "ART"),
    (28100, "UCH"),
    (29200, "SML"),
    (26300, "CSR"),
    (21000, "HUM"),
    (20504, "LCA"),
    (23500, "CHM"),
    (25200, "CEE"),
    (20200, "CLA"),
    (20300, "COM"),
    (25500, "COS"),
    (20503, "LCA"),
    (20400, "EAS"),
    (22200, "ECO"),
    (25400, "ECE"),
    (20600, "ENG"),
    (20700, "FIT"),
    (22700, "GSS"),
    (20800, "GER"),
    (26400, "HLS"),
    (22300, "HIS"),
    (20500, "LCA"),
    (24200, "LSI"),
    (21009, "HUM"),
    (23700, "MAT"),
    (21100, "MUS"),
    (21200, "NES"),
    (22500, "POL"),
    (27800, "PII"),
    (25800, "PSM"),
    (24400, "PNI"),
    (26000, "SPI"),
    (41400, "UAM"),
    (23900, "PSY"),
    (21400, "REL"),
    (21500, "SLA"),
    (22600, "SOC"),
    (21600, "SPO"),
    (20507, "LCA"),
    (20505, "LCA"),
]


def get_professors(number):
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
    # print("Access token:", access_token)
    data_url = BASE_URL + ENDPOINT + "?group=Department " + str(number) + " Faculty"

    response = requests.get(data_url, headers={"Authorization": auth_header})
    response_json_doc = json.loads(response.text)

    # Pretty-print the data.

    return response_json_doc


def print_professors(professors):
    for prof in professors:
        print(prof)


def add_professors(professors, dept):
    for prof in professors:
        add_professor(prof["full_name"], dept)


if __name__ == "__main__":
    for dept in DEPT_LIST:
        professors = get_professors(dept[0])
        # print(dept[1] + ": \n")
        # print_professors(professors)
        add_professors(professors, dept[1])
