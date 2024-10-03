#!/usr/bin/env python3

import argparse
import json
import requests
import sys
from parsel import Selector
import os
from datetime import datetime, timedelta

CORPS = []

# Function to check if .voltron_cookie file is older than 1 day
def check_cookie_file(file_path):
    if os.path.exists(file_path):
        file_mod_time = os.path.getmtime(file_path)
        file_mod_date = datetime.fromtimestamp(file_mod_time)
        current_date = datetime.now()

        # Check if the file is older than 1 day
        if current_date - file_mod_date > timedelta(days=1):
            return False
        return True
    else:
        return False

# Function to update .voltron_cookie file
def update_cookie_file(file_path):
    print("Your .voltron_cookie file is out of date. Please enter a new cookie value:")
    cookie = input("Enter new cookie: ")

    with open(file_path, 'w') as f:
        f.write(cookie)

# Function to read the cookie from .voltron_cookie
def get_cookie():
    cookie_file = ".voltron_cookie"
    if not check_cookie_file(cookie_file):
        update_cookie_file(cookie_file)
    
    try:
        with open(cookie_file, "r") as f:
            cookie = f.read().strip()
    except FileNotFoundError:
        print("Cookie file not found.")
        sys.exit()

    return cookie

# Function to make requests with the cookie
def request_url(url, **kwargs):
    cookie = get_cookie()
    headers = {"Cookie": str(cookie)}

    method = kwargs.get("method", None)
    data = kwargs.get("data", None)

    if method == "POST":
        r = requests.post(url, headers=headers, data=data)
    else:
        r = requests.get(url, headers=headers)
    return r

def get_single_group(name):
    r = request_url("https://garlic.beefalo.sigsci.net/groups/" + name)
    selector = Selector(text=r.text)
    displayname = selector.xpath('//input[@name="displayName"]/@value').get()
    description = selector.xpath('//input[@name="description"]/@value').get()

    group = {
        "displayName": displayname if displayname else "",
        "description": description if description else "",
    }

    return group

def get_corps():
    r = request_url("https://garlic.beefalo.sigsci.net/corps")
    selector = Selector(text=r.text)
    all_corps = []
    for tr in selector.css("#customer-corps > table > tbody > tr"):
        td = tr.xpath("./td[2]")
        corp_name = td.xpath("./a/text()").get()
        corp_url = td.xpath("./a/@href").get()
        corp = {"name": corp_name, "url": corp_url}
        all_corps.append(corp)

    for tr in selector.css("#staff-corps > table > tbody > tr"):
        td = tr.xpath("./td[2]")
        corp_name = td.xpath("./a/text()").get()
        corp_url = td.xpath("./a/@href").get()
        corp = {"name": corp_name, "url": corp_url}
        all_corps.append(corp)
    return all_corps

def find_corp(corp_name):
    corps = get_corps()
    for corp in corps:
        if corp["name"] == corp_name:
            return corp
    return None

def add_corp_to_groups(corp, groups):
    base_url = "https://garlic.beefalo.sigsci.net/groups/"

    if isinstance(corp, dict) and 'url' in corp:
        corp_id = corp["url"].split('/')[-1]
    else:
        raise ValueError(f"Invalid corp object: {corp}")

    for group in groups:
        print(f"Adding corp {corp['name']} to group {group}")
        groupdata = get_single_group(group)
        changes = {
            "corps": {"additions": {corp_id: True}, "deletions": {}},
            "sites": {"additions": {}, "deletions": {}},
            "users": {"additions": {}, "deletions": {}},
        }
        changesjson = json.dumps(changes)
        groupdata["changes"] = changesjson
        groupdata["action"] = "update"
        r = request_url(base_url + group, method="POST", data=groupdata)

def main(argv):
    parser = argparse.ArgumentParser(
        prog="Voltron Tool",
        description="Add corp to groups",
    )
    parser.add_argument("-c", "--corp", required=True, help="Corp name")
    parser.add_argument("-a", "--action", choices=["add"], required=True, help="Action to perform")
    parser.add_argument("-g", "--groups", nargs="+", required=True, help="Groups to add corp to")

    args = parser.parse_args()
    corp_name = args.corp
    action = args.action
    groups = args.groups

    if action == "add":
        corp = find_corp(corp_name)
        if corp:
            add_corp_to_groups(corp, groups)
        else:
            print(f"Corp '{corp_name}' not found.")

if __name__ == "__main__":
    main(sys.argv[1:])
