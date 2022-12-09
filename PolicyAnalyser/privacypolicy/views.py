from pickletools import string1
from tkinter import Variable
from typing import List
from django.db.models import Q
from ast import Str
from email.policy import Policy
from gettext import find
from math import fabs
from multiprocessing import context
from tempfile import template
from turtle import title
from urllib3 import request
import csv
from xdrlib import ConversionError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from google_play_scraper import app
from google_play_scraper import permissions
# from __future__ import unicode_literals, print_function
import js2py
import sqlite3
import os
import re

# from goose3 import Goose
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException
# PDF Conversion
# ------------------------------
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
# from django.conf import Settings
from django.conf import settings
from django.contrib.staticfiles import finders
# -------------------------------
# import pdfkit as pdf
# Create your views here.
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import array as arr
nlp = spacy.load('en_core_web_sm')
# pkgName= StringVar()
# policy_txt= StringVar()
# SELECT * FROM devAddress WHERE alias IS NOT NULL AND alias != ""
bold = "\33[1m"
policy_txt = ""
mysummary = ""
appImage = ""
appName = ""
devAddress = ""
devName = ""
email = ""
pdf = ""
downloads = ""
policyUrl = ""
fullLink = ""
words = ["Information", "IP Address", "email address", "First name", "last name", "Phone number", "Address", "Usage Data", "Caller ID", "messaging", "dialer", "device ID", "unique identifier", "device manufacturer",
         "device", "hardware settings", "SIM card", "Bank card", "Permanent Account Number", "Aadhaar card", "family details", "Mobile", "Facebook", "AdMob", "Google Play Services", "Storage", "Location", "SD CARD", ]
appPkg=""

def index(request):

    return render(request, 'index.html')


def home(request):
    global pkgName,appPkg
    global myList 
    myList= []
    if request.method == "POST":
        # global pkgName
        pkgName = request.POST['pkgName']
        if pkgName.find("https://") == -1:  # Package name search in playstore
            print('I have reached playstore via package name')
            homepage="homeplaystore.html"
            url = "https://play.google.com/store/apps/details?id={}&hl=en_IN&gl=US".format(pkgName)
            appPkg=pkgName
            print(url)
            context = googleScrapping(url)
        elif pkgName.find("google") != -1:  # link based search in playstore'
            print('I have reached playstore')
            homepage="homeplaystore.html"
            url = ""
            url = pkgName
            appPkg=url.split("https://play.google.com/store/apps/details?id=")[1]
            # pkgName=pkgName.strip("&hl=en_IN&gl=US")
            # print(appPkg)
            context = googleScrapping(url)

        elif pkgName.find("apple") != -1:  # app store search in playstore
            # url = ""
            homepage="homeappstore.html"
            url = pkgName
            idRegex = "[0-9][0-9][0-9]+"
            pkgName = re.findall(idRegex, pkgName)[0]         
            context = appStoreScrapp(url)
            print("found apple store link")
        else:
            print("please enter proper link to proceed")

        # print(url)
    return render(request,homepage, context)





def googleScrapping(url):
    global mysummary,appImage,appName ,devAddress, devName,email,pdf,policyUrl,fullLink,dataCollectUrl,mydownload,category,rating,devId
    mysummary,appImage,appName ,devAddress, devName,email,pdf,policyUrl,fullLink,dataCollectUrl,mydownload,category = "","","","","","","","","","","","",
    global variable3
    variable3 = "Developer's Address"
    dataCollectUrl="https://play.google.com/store/apps/datasafety?id="+appPkg
    appDetails= storeScrapper(appPkg)

    print(dataCollectUrl)
    # # if pkgName.find("apple.com") == -1:
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
               "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'en,en-US;q=0.5,en;q=0.3',
    # 'Referer': 'https://www.espncricinfo.com/',
    # 'Upgrade-Insecure-Requests': '1',
    # 'Connection': 'keep-alive',
    # 'Pragma': 'no-cache',
    # 'Cache-Control': 'no-cache',}
    r = requests.get(url, headers=headers , timeout=5)
    htmlContent = r.content

    bsoup = BeautifulSoup(htmlContent, 'html.parser')
    divs = bsoup.find_all('div', attrs={'class': "pSEeg"})
    ctr = 1
    rating=""
    for div in bsoup.find_all('div' , attrs={ "class" : "TT9eCd"}):
        print(div.text)
        rating=div.text
        rating= rating.replace("star" ,"")

    # To find the Developer Link and Scrape
    for link in bsoup.find_all('a' , attrs={ "class" : "WpHeLc VfPpkd-mRLv6"}):
        devString=""
        developrString=""
        devId=""
        myString=""
        devString= link.get('href')
        if(devString.find('dev') != -1):
            
            idRegex = "[0-9][0-9][0-9]+"
            
            myString = re.findall(idRegex,devString)
            devId=myString[0]
            devLink="https://play.google.com/store/apps/dev?id="
            developerLink=devLink + myString[0]
            developrString=developerLink
        elif(devString.find('developer') != -1):
             kstring=devString
             print(kstring)
             myString= kstring.lstrip("/store/apps/developer?id=")
             devId=appDetails()
            # if(devId == ""):
            #     devId ="No Developer Id number found"
            # print(myString)
            
       
            # print(developerLink)  
    
        if(devString.find('cluster') != -1):
            
            # idRegex = "[0-9][0-9][0-9]+"
            
            # myString = re.findall(idRegex,devString)
            # print(myString)
            
            othrLink="https://play.google.com"
            othrAppLink=othrLink+devString
            # print(othrAppLink)
            OthrAppString=othrAppLink
        
            print(OthrAppString) 
       
    # r = requests.get(developrString, headers=headers , timeout=5)
    # htmlContent = r.content  
    global devlopersApps
    devlopersApps=""
    if( developrString == ""):
        devlopersApps="No other application is found"
       
    else:
        devSoup=webSoup(developrString)
    
        
        for div in devSoup.find_all('div', attrs={'class': "Epkrse"}):
            print(div.text)
            if(devlopersApps.find(div.text)==-1):
                    devlopersApps = (devlopersApps + div.text +",")
                    # print(devlopersApps)
            # To find similar App Names of the same genre


    global otherApps
    otherApps=""
    # if(OthrAppString != ""):
    othrAppScrap=webSoup(OthrAppString)
    for div in othrAppScrap.find_all('div' , attrs={'class' : "Epkrse"} ):
            print(div.text)
            if(devlopersApps!=" No other application is found"):
                otherApps= (otherApps+div.text+" "+",")
            else:
               if(devlopersApps.find(div.text) == -1):
            # print .find('li', attrs={'title': ''})
            
                # if(link.string != "Browse Mac App Store" and link.string !="find a retailer"):
                otherApps= (otherApps+div.text+" "+",")
                # print(otherApps)
    for div in divs:
        # print (link.string)
        if(div):
            ctr = ctr+1

        if(ctr == len(divs)+1):
            # global policyUrl
            # policyUrl = div.text
            policyUrl=appDetails.get("privacyPolicy")
            print(div.text)
            if url_ok(policyUrl):
                session = requests.Session()
                session.verify = False
                r = requests.get(policyUrl, headers=headers)
                content = r.content
                soup = BeautifulSoup(content, 'html.parser')
                #     print(link.get("href"))
                #     newpath = 'D:\\python\\privacypolicy'
                global policy_txt
                policy_txt = ""
            if(policyUrl.find(".txt")!= -1):
                    policy_txt=soup.get_text()
                    mysummary = ""
                        # print(data.get_text())
                    mysummary = summarize(policy_txt, 0.08 ) #0.12)
            else:    
                for data in soup.find_all('p'):
                    policy_txt=policy_txt+data.get_text()
                    # print(type(data.get_text()))
                    # print(policy_txt)  
                    # policy_txt=policy_txt.strip()
                # finalsummary=policy_txt
                if policy_txt:
                        # global mysummary
                        mysummary = ""
                        # print(data.get_text())
                        mysummary = summarize(policy_txt, 0.08 ) #0.12)
                        # policy_txt=''+ mysummary
                        # print(mysummary)
                        
                        # mysummary = highlight_words(summary,words)
                else:
                        # policy_txt = "Not Found"
                        # mysummary = "Not Found"
                        print("URL is Up") 
            
            # print(mysummary)     
        # else:
        #     print("URL is Down")
        #     mysummary = "The privacy policy link is not working."

    # rctr = 1

        

        mydownload= appDetails.get('installs')
        category=appDetails.get('genre')
        devAddress=appDetails.get('developerAddress')
        devId=appDetails.get("developerId")
        if devAddress is None:
            devAddress = " No address found."
    # for mydiv in bsoup.find_all('div', attrs={'class': "ClM7O"}):
    #         # print (link.string)
            
    #         # mydivs = mydivs+mydiv.text
    #         if(rctr==2):
    #             # rctr = rctr + 1
    #         #  print(mydiv.text)  
    #         # if rctr == len(mydiv)+1:
    #             # print(mydiv.text)
    #             mydownload = mydiv.text
    #             print(mydownload)
    #         else :
    #            rctr = rctr+1

    # for div in bsoup.find_all('div', attrs={'class': "pSEeg"}):
    #     if div.text.find(",")!= -1 :
    #         # if div.text:
    #             # global devAddress
    #             devAddress = div.text
    #             print(devAddress)
    #         # else:
    #         #     devAddress = " No address found."

    #     elif div.text.find(" ")!=-1:
    #         # if div.text:
    #             # global devAddress
    #             devAddress = div.text
    #             print(devAddress)
    #     else:
    #             devAddress = " No address found."
        # else:
        #         devAddress = " No address found."
        

    
    for div in bsoup.find_all('div', attrs={'class': "pSEeg"}):

        if div.text.find("@")!= -1:
            if div.text :
                # global email
                email = div.text
                print(email)
            else:
                email = " No email address found."

                #  print (devAddress)

    # for div in bsoup.find_all('div',attrs={'class':"Mqg6jb Mhrnjf"}) or bsoup.find_all('div',attrs={'class':"wkMJlb YWi3ub"}) :   #Il7kR
    for item in bsoup.find_all('img', attrs={'class': "T75of cN0oRe fFmL2e"}):
        # print (div.text)
        # global appImage
        if bsoup.select_one("img")["src"]:
            appImage = ""
            # appImage = bsoup.select_one("img")["src"]
            appImage = item["src"]
            print(appImage)

        else:
            appImage = ""

        # global appName
        if bsoup.select_one("div h1 span").text:
            appName = bsoup.select_one("div h1 span").text
        else:
            appName = "Not found"

        print(appImage)

    for div in bsoup.find_all('div', attrs={'class': "tv4jIf"}):
        # if link.get("href").find("mailto:")!= -1:
        #     for j in range(3,sh1.max_row+1):
        #         sh1.cell(i,j,link.get("href").lstrip("mailto:"))
        #    print(link.get("href").lstrip("mailto:"))
        # if div.text.find(",") !=-1:
        #      global devAddress
        if bsoup.select_one("div a span").text:
            # global devName
            devName = bsoup.select_one("div a span").text
        else:
            devName = ""

        # print (devName)
    # for div in bsoup.find_all('div', attrs={'class': "ClM7O"}):
       
        # print(mydivs)
        # for mydiv in 
   

        # print(rctr)
            # print(mydiv)
            # print(mydiv.text)

        #  if bsoup.select_one("div").text :
        #      global devName
        #      devName = bsoup.select_one("div a span").text
        #  else :
        #      devName = ""

    
        
            # headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(dataCollectUrl ,headers= headers)
    dataCollectContent = r.content

    dataCollectsoup = BeautifulSoup(dataCollectContent, 'html.parser')
    global myList
    myList=""
    for div in dataCollectsoup.find_all('div',attrs={'class':"fozKzd"}):
                 if myList.find(div.text)==-1 :
                    myList=(myList+div.text +' , ')
                 

                    # print(myList)    
    if myList == '':      # print(hdr.text)
         myList="Application is not collecting any data"       
    myList= myList.split("Your data is transferred over a secure connection")[0]   
    global pdfpath
    # pdfpath="playstorepdf.html"
    pdfpath="homeplaystore.html"

    context = {
        "Variable": mysummary,
        "Variable2": pkgName,
        "Variable3": variable3,
        "appImage": appImage,
        "appName": appName,
        "devName": devName,
        "rating": rating,
        "text": devId,
        "downloads": mydownload,
        "policyURL": policyUrl,
        "address": devAddress,
         "myList": myList,
        "category": category,
        "devAppList" : devlopersApps ,
        "genreList" : otherApps,
        "email": email # soup.get_text()
    }
    return context


def appStoreScrapp(url):
    global mysummary,appImage,appName ,devAddress, devName,email,pdf,downloads,policyUrl,fullLink,appleCategory,rank
    mysummary,appImage,appName ,devAddress, devName,email,pdf,downloads,policyUrl,fullLink,appleCategory,rank= "","","","","","","","","","","","",
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
               "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    htmlContent = r.content

    bsoup = BeautifulSoup(htmlContent, 'html.parser')
    # print(bsoup.prettify)
    # title = bsoup.find(
    #     'h1', attrs={'class': "product-header__title app-header__title"})
    # print(bsoup.get_text())
    # print(title.getText(strip=True))
    global variable3
    variable3 = "Application ID"
    # global appName
    appliName= bsoup.select_one('h1').text
    global spanTxt
    spanTxt= bsoup.select_one('h1 span').text
    appName= appliName.replace(spanTxt,'')
    appName=appName.replace("\n" ,"")
    # appName = re.sub(r'\d+[+]', '', title.get_text(strip=True))
    # for h1 in bsoup.find_all('h1',attrs={'class':"product-header__titleapp-header__title"}):

    #    print(h1.get_text())
    # global devName
    devName = bsoup.find('a', attrs={'class': "link"}).getText()
    # policyUrl = bsoup.find( 'a', attrs={'class': "link icon icon-after icon-external"}).get('href')
    for link in bsoup.find_all('a', attrs={'class': "link"}):
      my_string=link.get('href')
    #   print(link.get('href'))
      if my_string.find('/genre/') !=-1:
           appleCategory= link.string
           appleGen= my_string
        #    global webScrap
           webScrap = webSoup(appleGen)
      
      if my_string.find('/developer/') !=-1:
           idRegex = "[0-9][0-9][0-9]+"
           global appleDev
           appleDev= re.findall(idRegex, my_string)[0]
           devScrap= webSoup(link.get('href'))
        #    print(devScrap.get_text())
          #    print(appleDev)
        
    # myText= devScrap.select_one('div')
    # print(myText.text)
    global devlopersApps
    devlopersApps=''
    if(appName):
       
        for item in devScrap.find_all('p') :
            if(devlopersApps.find(item.text)==-1 and devlopersApps.find(appName)==-1):
                devlopersApps = (devlopersApps + item.text +",")
                devlopersApps=devlopersApps.replace(appName,"")
        print(devlopersApps)
    # for div in devScrap.find_all('div', attrs={'class' : "we-clamp we-clamp--visual"}):
    #     for div1 in div:
    #         print(div1.text)

     ## This is used to get the all other apps of the same genre  
    global otherApps
    otherApps=""
    for link in webScrap.find_all('a' , attrs={'title': "",'class' : ""} ):
            
        app_String=link
        if(app_String.find('https://apps.apple.com/in/app/') != -1):
            # print .find('li', attrs={'title': ''})
            
            if(link.string != "Browse Mac App Store" and link.string !="find a retailer"):
                otherApps= (otherApps+link.string+" "+",")
              
        # print(otherApps)
     
   
    for link in bsoup.find_all('a'):


        if (link.text == "developer’s privacy policy"):
            # print(link.get("href"))
            # global policyUrl
            policyUrl = link.get("href")

            # print(url_ok(policyUrl))
            # global mysummary
            global policy_txt

            if url_ok(policyUrl):
                session = requests.Session()
                session.verify = False
                # headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
                           "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
                r = requests.get(policyUrl, headers=headers)
                content = r.content
                soup = BeautifulSoup(content, 'html.parser')
                # print(soup.get_text())

                policy_txt = soup.get_text()
                # print(policy_txt)
                if(getEmail(policy_txt)!=[]):
                   email=getEmail(policy_txt)[0]
                   print(email[0])
                else:
                   email="Not found"
                if soup.get_text():

                    # summary = ""
                    mysummary = summarize(soup.get_text(), 0.12)
                    if mysummary == "":
                        mysummary="Privacy Policy page is dynamic page. The analyser is unable to process "

                else:
                    policy_txt = "Not Found"
                    mysummary = "Not Found"
                print("URL is Up")
            else:
                print("URL is Down")
                mysummary = "The privacy policy link is either not working or have some security checks which is blocking to get the data."
    global myList
    myList =''
    

    for span in bsoup.find_all('span' , attrs={'class' : "privacy-type__grid-content privacy-type__data-category-heading"}) :

       
        if myList.find(span.text)==-1 :
          myList=(myList+span.text +' , ')
        

        # print(myList)    
        
    for image in bsoup.find_all('source'):
        # fullLink = image.get('srcset')
        # print(fullLink)
        # global appImage
        if image.get('srcset').find('/246x0w.webp') != -1:
            #  print(image)
            fullLink = image.get('srcset')
            fullLink = fullLink.split(" 246w,")
            print(fullLink[0])
            appImage = fullLink[0]
            #  print(imgSrc)
        # else :
            # appImage="Error"

        # rank= tag.text
    # global devAddress
    devAddress = " The developer address is not found"

    # for finding Rank of the application
    global apprank
    apprank=''
    for tag in bsoup.find_all('a', attrs={'class': "inline-list__item"}):
        # print(tag.text)
        # global downloads
        
        apprank=tag.text
    if apprank == "":    # This is for app store app ranking purpose
            rank="Not Available"     
    else:
           rank = apprank   
    #     emailregex = "\S+@\S+\.\S+"
    #     # global email
    #     email = ""
    #     email = re.findall(emailregex, bsoup.get_text())
    #     if email:
    #         email = email[0]
    #     else:
    #         email = "No email address found"

    # mail= mail[0].lstrip("#")
    # print(mail)
    # email=email[0].strip("-")
    global pdfpath
    pdfpath="appstorepdf.html"
    context = {
        "Variable": mysummary,
        "Variable2": pkgName,
        "Variable3": variable3,
        "appImage": appImage,
        "text": "Rating",
        "rank": rank,
        "appName": appName,
        "devName": devName,
        "address": pkgName,
        "policyURL": policyUrl,
        "downloads": spanTxt,
        "myList": myList,
        "devAppList" : devlopersApps ,
        "category" : appleCategory,
        "appleDevId" : appleDev,
        "genreList" : otherApps,
        "email": email  # soup.get_text()
    }
    return context


def summarize(text, per):

    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    # print(len(summary))
    # print(len(text))
    return summary


def showSummary(text):

    mysummary = summarize(text, 0.1)
    return mysummary


def download_txt(request):
    # response= HttpResponse(content_type ="text/plain")
    response = HttpResponse(content_type="application/pdf")

    response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(appName)
    #  To Write lines in text file
    response.write(policy_txt)
    return response


# def highlight_words(sentence, words):
#     for i in range(len(sentence)):
#         for j in range(len(words)):
#             if sentence.lower().startswith(words[j].lower(), i):
#                 sentence = sentence[:i] + sentence[i:i +
#                                                    len(words[j])].upper() + sentence[i+len(words[j]):]
#     return sentence


def render_pdf_view(request):

    if(pdfpath == "homeplaystore.html"):
        template_path = pdfpath
        sumTxt= sumModifier(mysummary)
    # context = {'myvar': 'this is your template context'}

        context = {
          "Variable": sumTxt,
          "Variable2": pkgName,
          "Variable3": variable3,
          "appImage": appImage,
           "appName": appName,
           "devName": devName,
            "rating": rating,
              "text": devId,
         "downloads": mydownload,
         "policyURL": policyUrl,
           "address": devAddress,
            "myList": myList,
          "category": category,
       "devAppList" : devlopersApps ,
        "genreList" : otherApps,
             "email": email # soup.get_text()
        }
    elif (pdfpath == "appstorepdf.html"):
        template_path = pdfpath
        context={
             "Variable": mysummary,
            "Variable2": pkgName,
            "Variable3": variable3,
            "appImage": appImage,
            "text": "Rating",
            "rank": rank,
            "appName": appName,
            "devName": devName,
            "address": pkgName,
            "policyURL": policyUrl,
            "downloads": spanTxt,
            "myList": myList,
            "devAppList" : devlopersApps ,
            "category" : appleCategory,
            "appleDevId" : appleDev,
            "genreList" : otherApps,
            "email": email  # soup.get_text()
        }
    
    # print("The context values are"+context)
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(appName)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def url_ok(url):

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
    #            "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    # exception block
    try:

        # session = requests.Session()
        # session.verify = False

        response = requests.get(url, headers=headers)
        # response = requests.head(url)

        # check the status code
        # print(response.status_code)
        if response.status_code == 200 and url.find("http://go.microsoft.com") == -1:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return e


def storeScrapper(PkgName):
    data=PkgName
    # if(url.find("https://play.google.com/store/apps/details?id=") != -1) :
    # appPkgName=url.strip('https://play.google.com/store/apps/details?id=')
    print(appPkg)
    # else:
    #     appPkgName=url
    #     print(appPkgName)
    result = app(
    data,
    lang='en', # defaults to 'en'
    country='in' # defaults to 'us' 
    )
   
    # print(result.get('title'))
    # print(result.get('installs'))
    # print(result.get('developer'))
    # print(result.get('developerEmail'))
    # print(result.get('developerWebsite'))
    # print(result.get('developerAddress'))
    # print(result.get('privacyPolicy'))

    # appDetails = permissions(
    # data,
    # lang='en', # defaults to 'en'
    # country='in', # defaults to 'us'
    # )
    return result   

def appDatabase():
  conn= sqlite3.connect('appdatabase.db')
  cur=conn.cursor
  cur.execute(''' CREATE TABLE Applist(p_id INTEGER PRIMARY KEY AUTOINCREMENT,p_name TEXT )''')


def webSoup(url):
      session = requests.Session()
      session.verify = False
      # headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
                           "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
      r = requests.get(url, headers=headers,)
      content = r.content
    #   print(content)
      webSoup = BeautifulSoup(content, 'html.parser')
    #   print(webSoup.prettify)         
      return webSoup

def getEmail(text):
    doc= nlp(text)
    emails=[]
    for token in doc:
        if token.like_email:
           emails.append(token.text)
    return emails

def sumModifier(text):
           
            from spacy.lang.en import English 
            # textToCompare = "Information"
            userInfo = { "information" :"<u>information</u>","ip address" :"<u>ip address</u>", "email address": "<u>email address</u>", "first name" :"<u>first name</u>", "last name" :"<u>last name</u>", "phone number" : "<u>phone number</u>", "address" : "<u>address</u>", "usage data" : "<u>usage data</u>" , "caller id" : "<u>Caller ID</u>" , "messaging" :"<u>messaging</u>" , "dialer":"<u>dialer</u>", "device id":"<u>device ID</u>", "unique identifier":"<u>unique identifier</u>", "device manufacturer":"<u>device manufacturer</u>", "device":"<u>device</u>", "hardware settings":"<u>hardware settings</u>", "sim card" :"<u>SIM card</u>", "bank card" :"<u>Bank card</u>", "permanent account number" : "<u>Permanent Account Number</u>", "aadhaar card" :"<u>Aadhaar card</u>", "family details" :"<u>family details</u>", "mobile":"<u>Mobile</u>", "facebook" :"<u>Facebook</u>", "admob": "<u>AdMob</u>", "google play services" :"<u>Google Play Services</u>", "storage" :"<u>Storage</u>", "location" :"<u>Location</u>", "sd card" :"<u>SD CARD</u>"}
            # let paragraph = document.getElementById("paragraph");
            # paragraphTxt = text

            # nlp = English()
            # nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
            doc = nlp(text)
            # sentences = [sent.string.strip() for sent in doc.sents]

            for sents in doc.sents:
                docSents=sents
                for search_text in userInfo:
                    replace_text= userInfo[search_text]
                    docSents=docSents.replace(search_text,replace_text)
                    paragraphTxt="".join(docSents)
                
            # paragraphTxt = paragraph.textContent.replace(pattern, match => `<mark id="info"><b>${match}</b></mark>`);

        #     for (i = 0; i <= userInfo.length; i++) {
        #     userInfo[i] = userInfo[i].replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        #     let pattern = new RegExp(`${userInfo[i]}`, "gi");
        #     // let color=["info","usrdata","usrdata","usrdata","usrdata","usrdata","usrdata","usrdata"];
        #     paragraphTxt = paragraphTxt.replace(pattern, match => `<mark><b>${match}</b></mark>`);
        # }'''
            return paragraphTxt