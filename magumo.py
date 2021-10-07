import os
from flask.wrappers import Response
import slack
from slackeventsapi import SlackEventAdapter

from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import cv2

#環境変数読み込み
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
#port = int(os.getenv('PORT')) #Heroku用 Port設定

app = Flask(__name__)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

url = 'https://tenki.jp/radar/1/'

@app.route('/ame', methods=['POST'])
def post_amagumo():
    data = request.form
    channel_id = data.get('channel_id')

    browser = webdriver.PhantomJS()
    browser.get(url)
    print('get url')
    browser.save_screenshot("tmp.png")

    img = cv2.imread("tmp.png")
    amagumofile = "Pictures/weather" + "amagumo.png"
    cv2.imwrite(amagumofile)

    client.chat_postMessage(channel=channel_id,text='テスト')
    client.files_upload(channel=channel_id,file=amagumofile)

    return Response(), 200

if __name__ == "__main__":
    app.run(debug = True)