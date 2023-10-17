from handler import sendMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import config
from datetime import datetime
from threading import Thread

# import telegrambot
from tkinter import Tk
import database


def setup():
    print(f"--->Setup selenium start : {str(datetime.now())}")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--force-dark-mode")
    chrome_options.add_argument("--window-size=1024,768")
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),options=chrome_options,
        )
    except Exception as e:
        print("Chrome doesn't exist")
        return "Chrome doesn't exist"
    print("Setup selenium complete")
    return driver


def screenshot(driver, chart, ticker="NONE", adjustment=0):
    print(f"--->Opening Chart {chart} : {str(datetime.now())}")

    chartUrl = (
        config.urls["tvchart"]
        + chart
        + "/"
        + (f"?symbol={ticker}" if ticker != "NONE" else "")
    )

    print(config.urls["tvchart"])
    print(chartUrl)
    driver.get(chartUrl)
    print("Sleep for 10 seconds - wait for chart to load")
    time.sleep(10)
    print("Adjusting position by ", adjustment)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()
    actions.send_keys(Keys.RIGHT * adjustment).perform()
    time.sleep(3)
    print("Chart is ready for capture")
    ActionChains(driver).key_down(Keys.ALT).key_down("s").key_up(Keys.ALT).perform()
    time.sleep(3)
    print("Chart is captured")
    return Tk().clipboard_get()


def quit_browser(driver):
    print(f"--->Exit browser : {str(datetime.now())}")
    driver.close()
    driver.quit()

def send_chart(chart, ticker, message, delivery):
    database.connect_to_database()
    driver = setup()
    if driver!="Chrome doesn't exist":
        driver.get("https://www.tradingview.com")
        # sessionId = db["sessionid"] if "sessionid" in db.keys() else "abcd"
        data = database.find_document_by_sessionid()
        sessionId = data["sessionid"] or "abcd"
        print("Session Id Used :", sessionId)
        driver.add_cookie(
            {"name": "sessionid", "value": sessionId, "domain": ".tradingview.com"}
        )
        screenshot_url = screenshot(driver, chart, ticker,)
        if delivery != "asap":
            sendMessage(message)
        sendMessage(screenshot_url)
        quit_browser(driver)
    else:
        return driver

def send_chart_async(chartUrl, ticker="NONE", message="", delivery="asap"):
    try:
        capture = Thread(target=send_chart, args=[chartUrl, ticker, message, delivery])
        capture.start()
    except Exception as e:
        print("[X] Capture error:\n>", e)
