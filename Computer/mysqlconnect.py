import os
import csv
import time
import json
import pymysql
import gspread
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from datetime import datetime
from matplotlib.font_manager import FontProperties
from oauth2client.service_account import ServiceAccountCredentials as SAC

def on_connect(client, userdata, flags, rc):
    print("connected")
    ansa0.configure(text="connected!",fg="green")
    client.subscribe("esp32/te/python")

def on_message(client, userdata, msg):
    now = datetime.now()
    print("從"+msg.topic+"  傳來  "+str(msg.payload))
    ansa4.configure(text=now.strftime("%Y-%m-%d %H:%M:%S"),fg="blue")
    ansa5.configure(text="Received data from Mqtt",fg="green")
    send_to_mysql(msg.payload.decode('utf-8'),now)
    up_google_sheet(msg.payload,now)

  

def up_google_sheet(data,time):
    auth_json_path = 'Your key'
    gss_scopes = ['https://spreadsheets.google.com/feeds']

    credentials = SAC.from_json_keyfile_name(auth_json_path,gss_scopes)
    gss_client = gspread.authorize(credentials)

    spreadsheet_key = 'Site Key'
    sheet = gss_client.open_by_key(spreadsheet_key).sheet1


    data = json.loads(data)
    temp = data["temp"]
    humid = data["humid"]

    print(type(temp))
    
    values = [temp,humid,time.strftime("%Y-%m-%d %H:%M:%S")]
    sheet.insert_row(values, 2)

    
def send_to_mysql(data,time):    
    data = json.loads(data)
    temperature = data["temp"]
    humidity = data["humid"]
    
    ansa1.configure(text="connected!",fg="green")
    ansa2.configure(text=str(temperature)+"°C",fg="blue")
    ansa3.configure(text=str(humidity)+"%",fg="blue")
    
    cursor = db.cursor()
    sql = "INSERT INTO python_dth11(temperature , humidity , time)VALUES (%s , %s , '%s')" % \
           (temperature,humidity,time)
    try:
       cursor.execute(sql)
       db.commit()
    except:
       db.rollback()
    ansa5.configure(text="Data in MySQL",fg="green")

def Search_data():
    SQL="SELECT * FROM python_dth11 order by time desc "
    #db.cursor.fetchall()
    cursor = db.cursor()
    cursor.execute(SQL)
    row = cursor.fetchone()
    print(row)
    db.commit()
    ansb1.configure(text=str(row[0])+"°C",fg="green")
    ansb2.configure(text=str(row[1])+"%",fg="green")
    ansb3.configure(text=row[2],fg="green")


def draw_temp_picture():
    point = int(box_value.get())
    myfont = FontProperties(fname='C:/Windows/Fonts/MSJH.ttc', size=20)# 字型選擇

    SQL="SELECT * FROM python_dth11 order by time desc "
    cursor = db.cursor()
    cursor.execute(SQL)
    row_n = cursor.fetchmany(point)
    db.commit()
    
    temp = []
    time = []
    
    for i in range(point):   
        temp.append(row_n[i][0])
        time.append(row_n[i][2])
    
    plt.figure('溫度監控視窗',figsize=(15,10),dpi=50,linewidth = 2)
    plt.plot(time,temp,'s-',color = 'r', label="MicroPython_DTH11")
    plt.title("近"+str(point)+"筆溫度變化表", fontproperties = myfont, x=0.5, y=1.03)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel("time", fontsize=30, labelpad = 15)
    plt.ylabel("temp", fontsize=30, labelpad = 20)
    
    plt.legend(loc = "upper right", fontsize=20)
    plt.show()

def draw_humid_picture():
    point = int(box_value.get())
    myfont = FontProperties(fname='C:/Windows/Fonts/MSJH.ttc', size=20)# 字型選擇

    SQL="SELECT * FROM python_dth11 order by time desc "
    cursor = db.cursor()
    cursor.execute(SQL)
    row_n = cursor.fetchmany(point)
    db.commit()
    
    humid = []
    time = []
    
    for i in range(point):   
        humid.append(row_n[i][1])
        time.append(row_n[i][2])
    
    
    plt.figure('濕度監控視窗',figsize=(15,10),dpi=50,linewidth = 2)
    plt.plot(time,humid,'s-',color = 'r', label="MicroPython_DTH11")
    plt.title("近"+str(point)+"筆濕度變化表", fontproperties = myfont, x=0.5, y=1.03)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel("time", fontsize=30, labelpad = 15)
    plt.ylabel("humid", fontsize=30, labelpad = 20)
    
    plt.legend(loc = "upper right", fontsize=20)
    plt.show()

def output_csv():
    SQL="SELECT * FROM python_dth11"
    cursor = db.cursor()
    cursor.execute(SQL)
    rows = cursor.fetchall()
    db.commit()
    
    window.filename =  filedialog.asksaveasfilename(initialdir = os.getcwd(),defaultextension=".csv",title = "選擇檔案儲存位置", filetypes = (("CSV files","*.csv"),("all files","*.*")))
    print (window.filename)
    
    fp = open(window.filename, 'wt')
    myFile = csv.writer(fp)
    myFile.writerows(rows)
    fp.close()
    print(os.path.dirname(window.filename))
    messagebox.showinfo('儲存成功', 'CSV已儲存')
    os.startfile(str(os.path.dirname(window.filename)))

def language_chinese():
    window.title("物聯網監控視窗")
    
    tab_control.add(tab1, text='即時監控')
    tab_control.add(tab2, text='MySQL最新資料查詢')
    tab_control.add(tab3, text='圖表與匯出')
    tab_control.add(tab4, text='詳細設定')
    
    lba0.configure(text="MQTT連線狀況 : ")
    lba1.configure(text="MySQL連線狀況 : ")
    lba2.configure(text="溫度(°C) : ")
    lba3.configure(text="濕度(%) : ")
    lba4.configure(text="收到資料時間 : ")
    lba5.configure(text="資料現在狀態 :  ")

    lbb1.configure(text="溫度(°C) : ")
    lbb2.configure(text="濕度(%) : ")
    lbb3.configure(text="最新資料時間 :  ")
    
    btnb1.configure(text="查詢")

    lbc1.configure(text="即時圖表")
    lbc2.configure(text="匯出CSV檔")

    btnc1.configure(text="溫度")
    btnc2.configure(text="濕度")
    btnc3.configure(text="儲存")

    lbd1.configure(text="即時圖表顯示資料數 : ")
    lbd2.configure(text="語言切換 : ")
    lbd3.configure(text="(預設為10筆)")
    lbd4.configure(text="視窗置頂 : ")

    btnd3.configure(text="開啟")
    btnd4.configure(text="關閉")
    
def language_english():
    window.title("IoT Surveillance System")
    
    tab_control.add(tab1, text='RTA')
    tab_control.add(tab2, text='MySQL Search')
    tab_control.add(tab3, text='Chart&Output')
    tab_control.add(tab4, text='Settings')

    lba0.configure(text="MQTT Status : ")
    lba1.configure(text="MySQL Status : ")
    lba2.configure(text="Temperature(°C) : ")
    lba3.configure(text="Humidity(%) : ")
    lba4.configure(text="Received Time : ")
    lba5.configure(text="Data Status :  ")

    lbb1.configure(text="Temperature(°C) : ")
    lbb2.configure(text="Humidity(%) : ")
    lbb3.configure(text="Latest Data Time:  ")
    btnb1.configure(text="Search")

    lbc1.configure(text="Chart")
    lbc2.configure(text="Export CSV")

    btnc1.configure(text="Temp")
    btnc2.configure(text="Humid")
    btnc3.configure(text="Save")

    lbd1.configure(text="Chart Of Data Point : ")
    lbd2.configure(text="Lauguage Change : ")
    lbd3.configure(text="(Default Value : 10)")
    lbd4.configure(text="Topmost Window : ")

    btnd3.configure(text="open")
    btnd4.configure(text="close")

def topwin_on():
    window.attributes('-topmost', True)

def topwin_off():
    window.attributes('-topmost', False)       
    

db = pymysql.connect("127.0.0.1","root","qweasdzxc","python_mqtt")


#視窗設定
window = Tk()
window.title("物聯網監控視窗")
window.geometry('400x250')

tab_control = ttk.Notebook(window)
tab_control.pack(expand=1, fill='both')

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

tab_control.add(tab1, text='即時監控')
tab_control.add(tab2, text='MySQL最新資料查詢')
tab_control.add(tab3, text='圖表與匯出')
tab_control.add(tab4, text='詳細設定')


#以下為第1個(tab)
lba0 = Label(tab1, text="MQTT連線狀況 : ")
lba1 = Label(tab1, text="MySQL連線狀況 : ")
lba2 = Label(tab1, text="溫度(°C) : ")
lba3 = Label(tab1, text="濕度(%) : ")
lba4 = Label(tab1, text="收到資料時間 : ")
lba5 = Label(tab1, text="資料現在狀態 :  ")

ansa0 = Label(tab1, text="not connect",fg="red")
ansa1 = Label(tab1, text="not connect",fg="red")
ansa2 = Label(tab1, text="N/A",fg="red")
ansa3 = Label(tab1, text="N/A",fg="red")
ansa4 = Label(tab1, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),fg="red")
ansa5 = Label(tab1, text="N/A",fg="red")


lba0.grid(column=1, row=0, sticky=E, padx=0, pady=5)
lba1.grid(column=4, row=0, sticky=E, padx=0, pady=5)
lba2.grid(column=1, row=1, sticky=E, padx=0, pady=10)
lba3.grid(column=1, row=2, sticky=E, padx=0, pady=10)
lba4.grid(column=1, row=3, sticky=E, padx=0, pady=10)
lba5.grid(column=1, row=4, sticky=E, padx=0, pady=10)

ansa0.grid(column=2, row=0, padx=0, pady=5, columnspan=2)
ansa1.grid(column=5, row=0, padx=0, pady=5, columnspan=2)
ansa2.grid(column=2, row=1, padx=0, pady=10, columnspan=2)
ansa3.grid(column=2, row=2, padx=0, pady=10, columnspan=2)
ansa4.grid(column=2, row=3, padx=0, pady=10, columnspan=2)
ansa5.grid(column=2, row=4, padx=0, pady=10, columnspan=2)


#以下為第2個(tab)
lbb1 = Label(tab2, text="溫度(°C) : ")
lbb2 = Label(tab2, text="濕度(%) : ")
lbb3 = Label(tab2, text="最新資料時間 :  ")

ansb1 = Label(tab2, text="N/A",fg="red")
ansb2 = Label(tab2, text="N/A",fg="red")
ansb3 = Label(tab2, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),fg="red")

btnb1 = Button(tab2, text="查詢",command=Search_data)

lbb1.grid(column=1, row=1, sticky=E, padx=0, pady=5)
lbb2.grid(column=1, row=2, sticky=E, padx=0, pady=10)
lbb3.grid(column=1, row=3, sticky=E, padx=0, pady=10)

ansb1.grid(column=2, row=1, padx=0, pady=5, columnspan=2)
ansb2.grid(column=2, row=2, padx=0, pady=10, columnspan=2)
ansb3.grid(column=2, row=3, padx=0, pady=10, columnspan=2)

btnb1.grid(column=2, row=5, padx=0, pady=10, columnspan=2)


#以下為第3個(tab)
lbc1 = Label(tab3, text="即時圖表")
lbc2 = Label(tab3, text="匯出CSV檔")


btnc1 = Button(tab3, text="溫度",command=draw_temp_picture)
btnc2 = Button(tab3, text="濕度",command=draw_humid_picture)
btnc3 = Button(tab3, text="儲存",command=output_csv)

lbc1.grid(column=1, row=0, sticky=E, padx=0, pady=5)
lbc2.grid(column=1, row=1, sticky=E, padx=0, pady=5)

btnc1.grid(column=2, row=0, padx=10, pady=10, columnspan=1)
btnc2.grid(column=3, row=0, padx=10, pady=10, columnspan=1)
btnc3.grid(column=2, row=1, padx=10, pady=10, columnspan=1)

#以下為第4個(tab)
lbd1 = Label(tab4, text="即時圖表顯示資料數 : ")
lbd2 = Label(tab4, text="語言切換 : ")
lbd3 = Label(tab4, text="(預設為10筆)")
lbd4 = Label(tab4, text="視窗置頂 : ")

btnd1 = Button(tab4, text="中文",command=language_chinese)
btnd2 = Button(tab4, text="English",command=language_english)
btnd3 = Button(tab4, text="開啟",command=topwin_on)
btnd4 = Button(tab4, text="關閉",command=topwin_off)

box_value = StringVar()
combod1 = ttk.Combobox(tab4,state="readonly",textvariable=box_value)
combod1['values']= (10, 15, 20, 25, 30)
combod1.current(0)

lbd1.grid(column=1, row=0, sticky=E, padx=10, pady=5)
lbd2.grid(column=1, row=1, sticky=E, padx=10, pady=5)
lbd3.grid(column=4, row=0, sticky=E, padx=15, pady=5)
lbd4.grid(column=1, row=2, sticky=E, padx=10, pady=5)

btnd1.grid(column=2, row=1, padx=10, pady=10, columnspan=1)
btnd2.grid(column=3, row=1, padx=10, pady=10, columnspan=1)
btnd3.grid(column=2, row=2, padx=10, pady=10, columnspan=1)
btnd4.grid(column=3, row=2, padx=10, pady=10, columnspan=1)

combod1.grid(column=2, row=0, columnspan=2)
#tkinter end

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqtt-dashboard.com", 1883, 60)
client.loop_start()
window.mainloop()
