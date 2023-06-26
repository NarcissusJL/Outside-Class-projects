#-*- encoding: utf-8 -*-
import pymysql
import datetime,time

#钉钉
import json
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#测试用URL
DingDingUrl = "https://oapi.dingtalk.com/robot/send?access_token=钉钉API接口串号"

def DingDingSendMessage(SendStr):
    global DingDingUrl
    yesterday = str(datetime.date.today()-datetime.timedelta(days=0))
    #构建一下请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    #构建请求数据
    data = {
        "msgtype": "text",
        "text": {
            "content": "今日 "+yesterday+"\n"+SendStr+"\n"
        },
        "at": {
             "isAtAll": True     #@全体成员（在此可设置@特定某人）
        }
    }
    #对请求的数据进行json封装
    sendData = json.dumps(data)#将字典类型数据转化为json格式
    sendData = sendData.encode("utf-8") # python3的Request要求data为byte类型
    #发送请求
    request = urllib.request.Request(url=DingDingUrl, data=sendData, headers=header)
    #将请求发回的数据构建成为文件格式
    opener = urllib.request.urlopen(request)
    #打印返回的结果
    #print(opener.read())

#缓冲时间
TempTime = ""
while True:
    today = str(datetime.date.today())

    #获取职工数据
    ConnMYSQL127 = pymysql.connect(host='localhost',db='covid19_teacher',port=3300,user='root',password='1233',use_unicode=True,charset='utf8')
    cursor127 = ConnMYSQL127.cursor()
    cursor127.execute("select * from everydatedata where AddDate='"+today+"' and DingDing='No' and (HealthCode!='绿' or TripCode!='绿')")
    results127 = cursor127.fetchall()
    if cursor127.rowcount>0:
        StrDing=""
        for Row127 in results127:
            StrDing=StrDing + str(Row127[0]) + " " + str(Row127[3]) + "\n　健康码：" + str(Row127[7]) + "　行程码：" + str(Row127[8]) +'\n\n'
            cursor127.execute("update everydatedata set DingDing='Yes' where AddDateTime='"+str(Row127[1])+"' and ID='"+str(Row127[0])+"'")
            ConnMYSQL127.commit()
            
        if StrDing != "":
            DingDingSendMessage(StrDing)
    results127 = None
    cursor127.close()
    ConnMYSQL127.close()

    #获取学生数据
    ConnMYSQL127 = pymysql.connect(host='localhost',db='covid19_gs',port=3300,user='root',password='1233',use_unicode=True,charset='utf8')
    cursor127 = ConnMYSQL127.cursor()
    cursor127.execute("select * from everydatedata where AddDate='"+today+"' and DingDing='No' and (HealthCode!='绿' or TripCode!='绿')")
    results127 = cursor127.fetchall()
    if cursor127.rowcount>0:
        StrDing=""
        for Row127 in results127:
            StrDing=StrDing + str(Row127[0]) + " " + str(Row127[3]) + "\n　健康码：" + str(Row127[7]) + "　行程码：" + str(Row127[8]) +'\n\n'
            cursor127.execute("update everydatedata set DingDing='Yes' where AddDateTime='"+str(Row127[1])+"' and ID='"+str(Row127[0])+"'")
            ConnMYSQL127.commit()
            
        if StrDing != "":
            DingDingSendMessage(StrDing)
    results127 = None
    cursor127.close()
    ConnMYSQL127.close()

    #获取学生数据
    ConnMYSQL127 = pymysql.connect(host='localhost',db='covid19_bk',port=3300,user='root',password='1233',use_unicode=True,charset='utf8')
    cursor127 = ConnMYSQL127.cursor()
    cursor127.execute("select * from everydatedata where AddDate='"+today+"' and DingDing='No' and (HealthCode!='绿' or TripCode!='绿')")
    results127 = cursor127.fetchall()
    if cursor127.rowcount>0:
        StrDing=""
        for Row127 in results127:
            StrDing=StrDing + str(Row127[0]) + " " + str(Row127[3]) + "\n　健康码：" + str(Row127[7]) + "　行程码：" + str(Row127[8]) +'\n\n'
            cursor127.execute("update everydatedata set DingDing='Yes' where AddDateTime='"+str(Row127[1])+"' and ID='"+str(Row127[0])+"'")
            ConnMYSQL127.commit()
            
        if StrDing != "":
            DingDingSendMessage(StrDing)
    results127 = None
    cursor127.close()
    
    ConnMYSQL127.close()
    
    time.sleep(60)


