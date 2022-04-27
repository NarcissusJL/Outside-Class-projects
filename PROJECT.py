#-*- encoding: utf-8 -*-
import pymysql
import datetime,time
import csv
import smtplib #加载smtplib模块
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

IsTest = "N"
yesterday = str(datetime.date.today()-datetime.timedelta(days=1))
today = str(datetime.date.today())

ConnMYSQL127 = pymysql.connect(host='localhost',db='covid19_bk',port=3300,user='root',password='1233',use_unicode=True,charset='utf8')

#获取部门列表
cursor127_department = ConnMYSQL127.cursor()
cursor127_department.execute("select * from department")
results127_department = cursor127_department.fetchall()
if cursor127_department.rowcount>0:
    for Row127_department in results127_department:
        print("部门："+Row127_department[0])

        #分割部门字符串
        DepartmentArr = Row127_department[4].split(",")
        DepartmentSQL = ""
        for DepartmentArrList in DepartmentArr:
            DepartmentSQL = DepartmentSQL + " or Department='"+ DepartmentArrList +"'"
        print(DepartmentSQL[3:])

        EmailMsg = ""
        EmailFiles = ""

        
        #今日未上报信息人员
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from user where AddDataDates not like '%"+today+"%' and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_未上报人员.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[1]),str(Row127_user[4])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　未上报人员错误")
            finally:
                csvFile.close()
                print("　　未上报人数："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "未上报人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_未上报人员.csv|"
        cursor127_user.close()
        

        #今日高温人员
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from everydatedata where AddDate='"+today+"' and Temperature='是' and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_高温人员.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级','体温'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[3]),str(Row127_user[20]),str(Row127_user[6])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　体温错误")
            finally:
                csvFile.close()
                print("　　高体温人数："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "高体温人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_高温人员.csv|"
        cursor127_user.close()


        #健康码非绿人员
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from everydatedata where AddDate='"+today+"' and HealthCode!='绿' and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_健康码.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级','健康码'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[3]),str(Row127_user[20]),str(Row127_user[7])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　健康码错误")
            finally:
                csvFile.close()
                print("　　健康码非绿人数："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "健康码非绿人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_健康码.csv|"
        cursor127_user.close()


        #通讯行程码非绿人员
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from everydatedata where AddDate='"+today+"' and (TripCode!='绿'or TripCodeStar='星') and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_通讯行程码.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级','通讯行程码','标记*号'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[3]),str(Row127_user[20]),str(Row127_user[8]),str(Row127_user[9])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　通讯行程码错误")
            finally:
                csvFile.close()
                print("　　通讯行程码异常人数："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "通讯行程码异常人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_通讯行程码.csv|"
        cursor127_user.close()


        #参与流调人员
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from everydatedata where AddDate='"+today+"' and Examine='是' and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_参与流调.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级','参与流调'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[3]),str(Row127_user[20]),str(Row127_user[10])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　参与流调错误")
            finally:
                csvFile.close()
                print("　　参与流调人数："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "参与流调人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_参与流调.csv|"
        cursor127_user.close()


        #当日不在津人员
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from everydatedata where AddDate='"+today+"' and InTianjin='否' and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_本人不在津.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级','不在津','出津日期','前往地点'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[3]),str(Row127_user[20]),str(Row127_user[11]),str(Row127_user[12]),str(Row127_user[13])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　不在津错误")
            finally:
                csvFile.close()
                print("　　本人不在津人数："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "本人不在津人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_本人不在津.csv|"
        cursor127_user.close()


        #其他情况
        cursor127_user = ConnMYSQL127.cursor()
        cursor127_user.execute("select * from everydatedata where AddDate='"+today+"' and other!='' and ("+ DepartmentSQL[3:] +") order by Department2")
        results127_user = cursor127_user.fetchall()
        if cursor127_user.rowcount>0:
            try:
                csvFile=open("D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_其他情况.csv",'w',newline='')
                writer=csv.writer(csvFile)
                writer.writerow(('序号','学号','姓名','班级','其他情况'))
                Xuhao = 1
                for Row127_user in results127_user:
                    writer.writerow((str(Xuhao),str(Row127_user[0]),str(Row127_user[3]),str(Row127_user[20]),str(Row127_user[18])))
                    Xuhao = Xuhao + 1
            except:
                print(Row127_department[0]+"　　其他情况错误")
            finally:
                csvFile.close()
                print("　　其他情况："+str(cursor127_user.rowcount))
                EmailMsg = EmailMsg + "有其他情况人数："+str(cursor127_user.rowcount)+"<br>"
                EmailFiles = EmailFiles + "D:/Python/CVS/bk/"+today+"_"+Row127_department[0]+"_其他情况.csv|"
        cursor127_user.close()


        time.sleep(1)
        #发送电子邮件
        sender = '发件箱地址'
        username = '发件箱地址'
        password = '发件箱密码'
        if IsTest=="Y":
            receiver = "接收邮箱"
        else:
            receiver = Row127_department[3]
        
        msg = MIMEMultipart() # 创建一个带附件的实例
        msg['Subject']=today + " 天医 " + Row127_department[0] + " 本科生健康信息（每日"+ time.strftime("%H",time.localtime()) +"时）异常情况" #邮件的主题，也可以说是标题
        msg.attach(MIMEText('天医'+ Row127_department[0] +'本科生健康信息（每日'+ time.strftime("%H",time.localtime()) +'时）异常情况信息，请查收附件。注：如果没有附件，则您部门全员没有异常情况。<br><br>'+EmailMsg, _subtype='html', _charset='utf-8'))

        for EmailFile in EmailFiles[0:-1].split("|"):
            #print(EmailFile)
            try:
                part = MIMEApplication(open(EmailFile, 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename = EmailFile[25:])
                msg.attach(part)
            except Exception:
                ret=' 失败！'
                print(ret)

        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.tmu.edu.cn') #发件人邮箱中的SMTP服务器
            smtp.login(username, password) #登陆服务器
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            ret=' 发送成功！'
        except Exception:  #如果try中的语句没有执行，则会执行下面的ret=False
            ret=' 发送邮件失败！！！'

        print("\r")
cursor127_department.close()

ConnMYSQL127.close()
print("完成")

