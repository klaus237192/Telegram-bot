# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : main.py                 #
# ----------------------------------------------- #

# External packages
from asyncio import run
import os
import json
import time

from flask import Flask, request
from tabulate import tabulate
import pandas as pd
from threading import Thread

# Internal packages
from captureutil import send_chart_async
from tradingview import login
import config
from handler import *

app = Flask(__name__)


def get_timestamp():
    return time.strftime("%Y-%m-%d %X")


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    try:
        jsonRequest = request.args.get("jsonRequest")
        chart = request.args.get("chart")
        tblfmt = request.args.get("tblfmt", default="plain")
        ticker = request.args.get("ticker", default="NONE")
        delivery = request.args.get("delivery", default="together")
        print(jsonRequest, chart, tblfmt, ticker, delivery)
        print("[I] Chart : ", chart)
        print("[I] Ticker : ", ticker)
        if request.method == "POST":
            print("This is post request")
            jsonPayload = request.get_json()
            key = jsonPayload["key"]
            if jsonRequest == "true" and key == config.sec_key:
                # jsonPayload = request.json
                # if "Custom" in jsonPayload["msg"]:
                #    chart = jsonPayload["msg"].pop("Custom")
                dataframe = pd.DataFrame(jsonPayload["msg"], index=[0]).transpose()
                payload = tabulate(dataframe, tablefmt=tblfmt)
            print("[I] Payload: \n", payload)
            if delivery == "asap" or chart is None:
                print(get_timestamp(), "Message Received & Sent!")
                sendMessage(payload)
            if chart != None:
                print(get_timestamp(), "Chart sent to telegram successfully")
                send_chart_async(chart, ticker, payload, delivery)
                return "success", 200
        else:
            print("Get request")
            return "Login is successful"
    except Exception as e:
        print("[X]", get_timestamp(), "Error:\n>", e)
        return "Error", 400


@app.route("/")
def main():
    print("Your bot is alive")
    return login()


def start_server_async():
    server = Thread(target=run)
    server.start()


def start_server():
    print("server is running at host=localhost, port=80...")
    from waitress import serve

    serve(app, host="0.0.0.0", port=80)
    print("server is suspended")


if __name__ == "__main__":
    start_server()
