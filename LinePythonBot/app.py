from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import time
from datetime import datetime
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('YourAPI')
# Channel Secret
handler = WebhookHandler('YourWebhookHandler')

def serach_temp_data():
    auth_json_path = 'mykey.json'
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
    gss_client = gspread.authorize(credentials)

    #開啟 Google Sheet 資料表
    spreadsheet_key = 'Your site'
    sheet = gss_client.open_by_key(spreadsheet_key).sheet1
    data = sheet.acell('A2').value
    now = sheet.acell('C2').value
    qwe = "溫度 : " + data + " °C\n\n" + "資料更新時間 : " + str(now)
    
    return qwe

def serach_humid_data():
    auth_json_path = 'mykey.json'
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
    gss_client = gspread.authorize(credentials)

    #開啟 Google Sheet 資料表
    spreadsheet_key = 'Your site'
    sheet = gss_client.open_by_key(spreadsheet_key).sheet1
    data = sheet.acell('B2').value
    now = sheet.acell('C2').value
    qwe = "濕度 : " + data + " %\n\n" + "資料更新時間 : " + str(now)
    return qwe

def prize():
    miss = 0
    win = 0
    glod = 0
    for i in range(10):
        a = random.randint(0,999)
        if a < 600 :
            if a < 30:
                win = win+1
            else:
                glod = glod+1
        else :
            miss = miss +1
    return "機率3%，此為十連抽" + "\n\n你獲得 : " + str(win) +"隻限定和"+str(glod)+"金"     


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if(text == "查詢溫度"):
        reply_text = serach_temp_data()
    elif(text == "查詢濕度"):
        reply_text = serach_humid_data()
    elif(text == "抽卡"):
        reply_text = prize()
    elif(text == "!連結"):
        reply_text = "此次期末Code" + "還沒處理好"
    #else:
      #  reply_text = text
        
    
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)
                              
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 

                              
                              
