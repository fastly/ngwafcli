#!/usr/bin/env python3

import argparse

# import getopt
import json
import os.path
import requests
import sys
import time
from parsel import Selector
from multiprocessing.pool import ThreadPool

CORPS = []
GROUPS = []
CURCOUNT = 0
COUNTCORPS = 0
COUNTGROUPS = 0
CURTYPE = ""


def request_url(url, **kwargs):
    try:
        with open(".env", "rb") as f:
            cookie = f.read()
    except FileNotFoundError:
        print("Requires cooke")
        sys.exit()
    headers = {"Cookie": str(cookie)}

    method = kwargs.get("method", None)
    data = kwargs.get("data", None)

    if method == "POST":
        # print(method, data)
        r = requests.post(url, headers=headers, data=data)
    else:
        r = requests.get(url, headers=headers)
    return r


def associate_groups_to_corps(all_corp_groups):
    global CORPS
    for v in all_corp_groups:
        for k, c in enumerate(CORPS):
            if c["name"] == v["corp"]:
                if v["group"] not in CORPS[k]["groups"]:
                    CORPS[k]["groups"].append(v["group"])


def get_single_group(name):
    r = request_url("https://garlic.beefalo.sigsci.net/groups/" + name)
    selector = Selector(text=r.text)
    displayname = selector.xpath('//input[@name="displayName"]/@value').get()
    description = selector.xpath('//input[@name="description"]/@value').get()
    betastatus = selector.xpath(
        '//select[@name="beta-status"]/option[@selected]/@value'
    ).get()
    betaname = selector.xpath('//input[@name="beta-name"]/@value').get()
    betadescription = selector.xpath('//input[@name="beta-description"]/@value').get()

    group = {}
    group["displayName"] = displayname if displayname != None else ""
    group["description"] = description if description != None else ""
    group["beta-status"] = betastatus if betastatus != None else ""
    group["beta-name"] = betaname if betaname != None else ""
    group["beta-description"] = betadescription if betadescription != None else ""

    return group


def get_corp_group_td(selector, find_str):
    return selector.xpath(
        '//th[text() = "{}"]/following-sibling::td/text()'.format(find_str)
    ).get()


def get_corp_groups():
    urls = [
        "https://garlic.beefalo.sigsci.net/domains/corp-groups",
        "https://garlic.beefalo.sigsci.net/domains/site-groups",
    ]
    all_corp_groups = []
    for u in urls:
        r = request_url(u)
        selector = Selector(text=r.text)

        for tr in selector.css("#table > table > tbody > tr"):
            row = {}
            td_all = tr.xpath(".//td/text()")
            if "/" in td_all[0].get():
                row["corp"] = td_all[0].get().split("/")[0]
            else:
                row["corp"] = td_all[0].get()
            row["group"] = td_all[2].get()
            all_corp_groups.append(row)
    return all_corp_groups


def get_corp_users(corp_name, selector_corp, xpath):
    trs = selector_corp.xpath(xpath)
    users = []
    try:
        for tr in trs:
            email = tr.xpath("./td[1]/a//text()").get()
            name = tr.xpath("./td[2]//text()").get()
            sso = tr.xpath("./td[5]//text()").get()
            api = tr.xpath("./td[7]//text()").get()
            users.append(
                {
                    "email": email,
                    "name": name,
                    "sso": sso.strip(),
                    "apiuser": api.strip(),
                }
            )
    except:
        pass
    return users


def get_single_corp(name, url, staff):
    r = request_url("https://garlic.beefalo.sigsci.net" + url)
    selector_corp = Selector(text=r.text)
    account_type = get_corp_td(selector_corp, "Account Type (via Salesforce)")
    site_used = get_corp_td(selector_corp, "Sites Configured")
    site_limit = get_corp_td(selector_corp, "Site Limit")
    created_on = get_corp_td(selector_corp, "Created On")
    last_updated = get_corp_td(selector_corp, "Last Updated")
    max_ratelimit_rules = get_corp_td(selector_corp, "Max Site Rate Limit Rules")
    auth_type = get_corp_td(selector_corp, "Auth Type")
    corp_data_table = selector_corp.xpath('//div[@class="col-md-7"]')
    if not max_ratelimit_rules:
        max_ratelimit_rules = 15
    users = get_corp_users(
        name,
        selector_corp,
        '//h3[text() = "Users "]/following-sibling::node()[2]/tbody/tr',
    )
    corp = {
        "name": name,
        "id": url.split("/")[-1],
        "staff": staff,
        "account_type": account_type,
        "auth_type": auth_type,
        "sites_used": int(site_used),
        "sites_limit": int(site_limit),
        "max_ratelimit_rules": int(max_ratelimit_rules),
        "created_on": created_on,
        "last_updated": last_updated,
        "users": users,
        "groups": [],
    }
    return corp


def get_corps(selector):
    global COUNTCORPS
    all_corps = []
    for tr in selector.css("#customer-corps > table > tbody > tr"):
        td = tr.xpath("./td[2]")
        corp_name = td.xpath("./a/text()").get()
        corp_url = td.xpath("./a/@href").get()
        corp = {"name": corp_name, "url": corp_url, "staff": False}
        all_corps.append(corp)

    for tr in selector.css("#staff-corps > table > tbody > tr"):
        td = tr.xpath("./td[2]")
        corp_name = td.xpath("./a/text()").get()
        corp_url = td.xpath("./a/@href").get()
        corp = {"name": corp_name, "url": corp_url, "staff": True}
        all_corps.append(corp)
    COUNTCORPS = len(all_corps)
    return all_corps


def get_groups():
    global COUNTGROUPS
    r = request_url("https://garlic.beefalo.sigsci.net/groups")
    selector = Selector(text=r.text)
    all_groups = []

    for c in selector.xpath("//code/text()"):
        #    group = get_single_group(c.get())
        all_groups.append(c.get())
    COUNTGROUPS = len(all_groups)
    return all_groups


def get_corp_td(selector, find_str):
    return selector.xpath(
        '//th[text() = "{}"]/following-sibling::td/text()'.format(find_str)
    ).get()


def write_cache(data, t):
    with open("{}.cache".format(t), "w") as f:
        f.write(json.dumps(data))


def read_corp_cache():
    with open("corp.cache", "r+") as f:
        raw_data = f.read()
        json_data = json.loads(raw_data)
        return json_data


def task(value, t):
    global CORPS
    global GROUPS
    global CURCOUNT

    if t == "corp":
        corp = get_single_corp(value["name"], value["url"], value["staff"])
        CORPS.append(corp)
        CURCOUNT += 1
    if t == "group":
        group = get_single_group(value)
        GROUPS.append(group)
        CURCOUNT += 1
    return CURCOUNT


def find_corp(value):
    global CORPS
    try:
        corp = next(item for item in CORPS if item["id"] == value)

        if len(corp) > 0:
            return corp
    except StopIteration:
        pass

    try:
        corp = next(item for item in CORPS if item["name"] == value)
        if len(corp) > 0:
            return corp
    except StopIteration:
        pass

    return "corp not found"


def match_filter_corp(field, oper, val):
    match oper:
        case "==":
            if field == val:
                return True
        case "!=":
            if field != val:
                return True
        case ">=":
            if field >= val:
                return True
        case "<=":
            if field <= val:
                return True
    return False


def find_users(userfilter):
    global CORPS
    output = []
    if userfilter != None:
        for corp in CORPS:
            try:
                for user in corp["users"]:
                    found_num = len(userfilter)
                    for f in userfilter:
                        skip_matcher = False
                        field = f["field"]
                        oper = f["oper"]
                        val = f["value"]
                        if match_filter_corp(user[field], oper, val):
                            found_num -= 1
                    if found_num == 0:
                        user["corp_name"] = corp["name"]
                        user["corp_id"] = corp["id"]
                        user["staff"] = corp["staff"]
                        output.append(user)

            except KeyError:
                pass
    return output


def find_corps(corpfilter):
    global CORPS
    output = []

    if corpfilter != None:
        for corp in CORPS:
            found_num = len(corpfilter)
            for f in corpfilter:
                skip_matcher = False
                field = f["field"]
                oper = f["oper"]
                val = f["value"]

                try:
                    if isinstance(corp[field], list):
                        list_len = len(corp[field])
                        if list_len == 0:
                            skip_matcher = True
                        for v in corp[field]:
                            if match_filter_corp(v, oper, val):
                                if oper != "!=":
                                    found_num -= 1
                                else:
                                    list_len -= 1
                        if oper == "!=" and not skip_matcher:
                            if list_len == 0:
                                found_num -= 1
                        if oper == "!=" and skip_matcher:
                            found_num -= 1
                    else:
                        if match_filter_corp(corp[field], oper, val):
                            found_num -= 1

                except KeyError:
                    pass
            if found_num == 0:
                output.append(corp["name"])
    else:
        for corp in CORPS:
            output.append(corp["name"])
    return output


def find_group(groups, group_oper):
    global CORPS
    corp_groups = {}
    for corp in CORPS:
        if not corp["staff"]:
            for group in groups:
                try:
                    if group in corp["groups"]:
                        if corp["name"] in corp_groups.keys():
                            corp_groups[corp["name"]]["count"] += 1
                        else:
                            corp_groups[corp["name"]] = {"count": 1}
                except KeyError:
                    pass

    if group_oper == "and":
        return [k for k, corp in corp_groups.items() if corp["count"] == len(groups)]

    return corp_groups.keys()


def add_corp_to_groups(corp, groups):
    base_url = "https://garlic.beefalo.sigsci.net/groups/"

    for group in groups:
        groupdata = get_single_group(group)
        changes = {
            "corps": {"additions": {corp["id"]: True}, "deletions": {}},
            "sites": {"additions": {}, "deletions": {}},
            "users": {"additions": {}, "deletions": {}},
        }
        changesjson = json.dumps(changes)
        groupdata["changes"] = changesjson
        groupdata["action"] = "update"
        r = request_url(base_url + group, method="POST", data=groupdata)


def progress_error(r):
    print("Error: ", r)


def progress(results):
    global COUNTCORPS
    global COUNTGROUPS
    global CURTYPE
    count = 0
    spin = ["⠇", "⠏", "⠋", "⠉", "⠙", "⠹", "⠸", "⠼", "⠴", "⠤", "⠦"]

    if CURTYPE == "corp":
        count = COUNTCORPS
    elif CURTYPE == "group":
        count = COUNTGROUPS

    print(
        "{}/{} {}".format(CURCOUNT, count, spin[(CURCOUNT % 11)]),
        end="\r",
        flush=True,
    )


def main(argv):
    global CORPS
    global GROUPS
    global CURTYPE

    old_cache = False
    rebuild = False

    parser = argparse.ArgumentParser(
        prog="Voltron Tool",
        description="Allows for searching and automating common Voltron tasks",
    )
    parser.add_argument("-a", "--action", choices=["get", "add"], default="get")
    parser.add_argument("-c", "--corp")
    parser.add_argument("-cf", "--corp-filter", help="accepts JSON filter")
    parser.add_argument("-uf", "--user-filter", help="accepts JSON filter")
    parser.add_argument("-g", "--groups", nargs="+")
    parser.add_argument("-go", "--group-oper", choices=["and", "or"], default="or")
    parser.add_argument("-r", "--rebuild", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "-rg", "--rebuild-groups", action=argparse.BooleanOptionalAction
    )
    args = parser.parse_args()
    action = args.action
    corp = args.corp
    if args.corp_filter:
        corpfilter = json.loads(args.corp_filter)
    if args.user_filter:
        userfilter = json.loads(args.user_filter)
    groups = args.groups
    group_oper = args.group_oper
    rebuild = args.rebuild
    rebuild_groups = args.rebuild_groups
    try:
        if time.time() - os.path.getmtime("corp.cache") >= 86400:
            old_cache = True
        else:
            CORPS = read_corp_cache()

    except FileNotFoundError:
        old_cache = True
        pass

    if old_cache or rebuild:
        print("Regenerating Corp cache")
        r = request_url("https://garlic.beefalo.sigsci.net/corps")
        selector = Selector(text=r.text)
        all_corps = get_corps(selector)
        CURTYPE = "corp"

        with ThreadPool() as pool:
            results = [
                pool.apply_async(
                    task,
                    args=(
                        value,
                        "corp",
                    ),
                    callback=progress,
                )
                for value in all_corps
            ]
            pool.close()
            pool.join()
        all_corp_groups = get_corp_groups()
        associate_groups_to_corps(all_corp_groups)
        write_cache(CORPS, "corp")
        print("\r")
    if rebuild_groups:
        CURCOUNT = 0
        CURTYPE = "group"
        print("Regenerating Group cache")
        all_groups = get_groups()
        with ThreadPool() as pool:
            results = [
                pool.apply_async(
                    task,
                    args=(
                        value,
                        "group",
                    ),
                    callback=progress,
                    error_callback=progress_error,
                )
                for value in all_groups
            ]
            pool.close()
            pool.join()

        write_cache(GROUPS, "group")
    try:
        if corp != None:
            if action != None:
                if action == "get":
                    if corp == "all":
                        print(json.dumps(find_corps(corpfilter), indent=2))
                    else:
                        print(json.dumps(find_corp(corp), indent=2))
                if action == "add":
                    if groups != None:
                        add_corp_to_groups(find_corp(corp), groups)
    except UnboundLocalError:
        pass

    try:
        if len(userfilter) >= 0:
            print(json.dumps(find_users(userfilter), indent=2))
    except UnboundLocalError:
        pass

    try:
        if groups != None:
            if group_oper in ["and", "or"] and action != "add":
                all_corp_groups = list(find_group(groups, group_oper))
                print(json.dumps(all_corp_groups, indent=2))
    except UnboundLocalError:
        pass
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
