import os
import sqlite3

firefox_path = os.path.join("C:", os.sep, "Users", "Arpit", "AppData", "Roaming", "Mozilla", "Firefox", "Profiles",
                            "d1oah1yg.Default User", "places.sqlite")
chrome_path = os.path.join("C:", os.sep, "Users", "Arpit", "AppData", "Local", "Google", "Chrome", "User Data",
                           "Default", "History")

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/open", methods=['GET'])
def open_browser():
    if request.args['browser'] == 'chrome':
        os.system("start chrome" + " " + request.args['url'])
    else:
        os.system("start firefox" + " " + request.args['url'])
    return jsonify(
        message='Browser Started',
        category="success",
        status=200
    )


@app.route("/stop/<string:browser>", methods=['GET'])
def stop_browser(browser):
    if browser == 'chrome':
        os.system("taskkill /IM chrome.exe /F")
    else:
        os.system("taskkill /IM firefox.exe /F")
    return jsonify(
        message='Browser Stopped',
        category="success",
        status=200
    )


@app.route("/cleanup/<string:browser>", methods=['GET'])
def cleanup_browser(browser):
    if browser == 'chrome':
        os.remove(chrome_path)
    else:
        os.remove(firefox_path)
    return jsonify(
        message='Browser Data Deleted',
        category="success",
        status=200
    )


@app.route("/geturl/<string:browser>", methods=['GET'])
def geturl_browser(browser):
    if browser == 'chrome':
        conn = sqlite3.connect(chrome_path, check_same_thread=False)
        c = conn.cursor()
        c.execute('SELECT url FROM urls where last_visit_time=(select max(last_visit_time) from urls)')
        web_site = c.fetchall()
        conn.close()
        return jsonify(
            last_visited_url=web_site,
            category="success",
            status=200
        )
    elif browser == 'firefox':
        conn = sqlite3.connect(firefox_path, check_same_thread=False)
        c = conn.cursor()
        c.execute('SELECT * FROM moz_origins')
        websites_list = c.fetchall()
        active_website = websites_list[-1]
        host = active_website[1]
        endpoint = active_website[2]
        conn.close()
        return jsonify(
            last_visited_url=host + endpoint,
            category="success",
            status=200
        )
