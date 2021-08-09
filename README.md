# Python小專題(MQTT溫溼度感測&大數據整理)

## 簡介
  透過ESP32+溫溼度感測器，將數值傳送到電腦端，電腦在將數值進行處理存入MySQL，並且使其可以透過電腦介面或Linebot來去做最新的溫溼度查詢，使用到的工具有
  1. MySQL
  2. MicroPython
  3. Python
  4. MQTT
  5. LineBot
  6. Heroku

## 介面預覽
![LineBot](https://github.com/Relhely/python_final_exam/blob/master/Picture/%E5%9C%96%E7%89%871.png)
![PC1](https://github.com/Relhely/python_final_exam/blob/master/Picture/%E5%9C%96%E7%89%872.png)
![PC2](https://github.com/Relhely/python_final_exam/blob/master/Picture/%E5%9C%96%E7%89%873.png)


## 流程
  這個專題內的重點最主要是如何將蒐集到的資料去做一個彙整，將資料彙整到MySQL後要如何提取出來和繪製成表格
  而至於後面的LineBot則比較像是單純的能將我們所蒐集到的資料去做一個應用，能隨時地去做查詢

## 注意點
  在此專案中的一些小部分需要注意，像是LineBot的金鑰、MySQL的權限和語法


## Python_Final_Exam
This is my python class final exam.  Use Mqtt&amp;MySQL to example  


MicroPython References :  
1.http://yhhuang1966.blogspot.com/2019/07/micropython-on-esp32.html   
2.http://yhhuang1966.blogspot.com/2017/05/micropython-on-esp8266_18.html  
3.http://yhhuang1966.blogspot.com/2019/06/esp32-micropython.html  

Line Bot :  
1.line code : https://blackmaple.me/line-bot-tutorial/  
2.Server Site : https://dashboard.heroku.com/  

Computer References(MySQL、Tkinter、GoogleSheet) :  
1.Tkinter : https://likegeeks.com/python-gui-examples-tkinter-tutorial/  
2.MySQL : https://www.runoob.com/python3/python3-mysql.html  
3.Google Sheet : https://medium.com/@yanweiliu/如何透過python建立google表單-使用google-sheet-api-314927f7a601



