import os
from database import connect_to_database, find_document_by_sessionid, insert_document
import requests
import platform
from urllib3 import encode_multipart_formdata
import config


def login():
    # sourcery skip: extract-method, inline-variable, use-fstring-for-concatenation

    collection = connect_to_database()
    test = {}
    # sessionid =  db["sessionid"] if 'sessionid' in db.keys() else 'abcd'
    # data = response.json()                                                                                                        #added
    # print(data)
    data = find_document_by_sessionid()
    if data != None:
        sessionid = data["sessionid"]
        headers = {"cookie": "sessionid={sessionid}"}
        test = requests.request("GET", config.urls["tvcoins"], headers=headers)
        print(test.text)
        if test.status_code == 200:
            return "login is successful"
    print("Database doesn't have sessionid\n")
    try:
        if "sessionid" in os.environ:
            print("SessionId from secrets :" + os.environ["sessionid"])
            headers = {"cookie": "sessionid=" + os.environ["sessionid"]}
            test = requests.request("GET", config.urls["tvcoins"], headers=headers)
            print(test.text)
            if test.status_code == 200:
                # sessionid = os.environ["sessionid"]
                return "login is successful"
    except Exception as e:
        print("OS.environ doesn't have sessionid")
    print(config.username, config.password)
    try:
        if config.username and config.password:
            print("session id from db is invalid")
            username = config.username
            password = config.password

            payload = {"username": username, "password": password, "remember": "on"}
            body, contentType = encode_multipart_formdata(payload)
            userAgent = f"TWAPI/3.0 ( {platform.system()}; { platform.version()};{ platform.release()} )"
            print(userAgent)
            login_headers = {
                "origin": "https://www.tradingview.com",
                "User-Agent": userAgent,
                "Content-Type": contentType,
                "referer": "https://www.tradingview.com",
            }
            login = requests.post(
                config.urls["signin"], data=body, headers=login_headers
            )
            cookies = login.cookies.get_dict()
            sessionid = cookies["sessionid"]
            # db["sessionid"] = sessionidc
            document = {"sessionid": sessionid}
            insert_document(document)
            print(document)
            return "login is successful"
    except Exception as e:
        print("username and password doesn't exist or network error\n", e)
        return "login is not successful"
