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
from urllib import request
import csv
from xdrlib import ConversionError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup

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
            url = "https://play.google.com/store/apps/details?id={}&hl=en_IN&gl=US".format(pkgName)
            print(url)
            context = googleScrapping(url)
        elif pkgName.find("google") != -1:  # link based search in playstore'
            # url = ""
            url = pkgName
            appPkg=url.split("https://play.google.com/store/apps/details?id=")[1]
            # pkgName=pkgName.strip("&hl=en_IN&gl=US")
            print(appPkg)
            context = googleScrapping(url)

        elif pkgName.find("app") != -1:  # app store search in playstore
            # url = ""
            url = pkgName
            idRegex = "[0-9]+"
            pkgName = re.findall(idRegex, pkgName)[0]
            context = appStoreScrapp(url)
            print("found apple store link")
        else:
            print("please enter proper link to proceed")

        print(url)
    return render(request, 'home.html', context)


def googleScrapping(url):
    global mysummary,appImage,appName ,devAddress, devName,email,pdf,policyUrl,fullLink,dataCollectUrl
    mysummary,appImage,appName ,devAddress, devName,email,pdf,policyUrl,fullLink,dataCollectUrl  = "","","","","","","","","",""
    global variable3,downloads
    variable3 = "Developer's Address"
    dataCollectUrl="https://play.google.com/store/apps/datasafety?id="+appPkg
    print(dataCollectUrl)
    # # if pkgName.find("apple.com") == -1:
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
               "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers , timeout=5)
    htmlContent = r.content

    bsoup = BeautifulSoup(htmlContent, 'html.parser')
    divs = bsoup.find_all('div', attrs={'class': "pSEeg"})
    ctr = 1

    for div in divs:
        # print (link.string)
        if(div):
            ctr = ctr+1

        if(ctr == len(divs)+1):
            # global policyUrl
            policyUrl = div.text
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
                policy_txt = soup.get_text()
                if soup.get_text():
                    # global mysummary
                    mysummary = ""
                    mysummary = summarize(soup.get_text(), 0.12)
                    # mysummary = highlight_words(summary,words)
                else:
                    policy_txt = "Not Found"
                    mysummary = "Not Found"
                    print("URL is Up")
        else:
            print("URL is Down")
            mysummary = "The privacy policy link is not working."

    rctr = 1
    for mydiv in bsoup.find_all('div', attrs={'class': "ClM7O"}):
            # print (link.string)
            
            # mydivs = mydivs+mydiv.text
            if(mydiv):
                rctr = rctr + 1
            # print(mydiv.text)  
            # if rctr == len(mydiv)+1:
                print(mydiv.text)
                downloads = mydiv.text
                # print(downloads)
            else :
               rctr = rctr+1

    for div in bsoup.find_all('div', attrs={'class': "pSEeg"}):
        if div.text.find(",")!= -1 :
            # if div.text:
                # global devAddress
                devAddress = div.text
                print(devAddress)
            # else:
            #     devAddress = " No address found."

        elif div.text.find(" ")!=-1:
            # if div.text:
                # global devAddress
                devAddress = div.text
                print(devAddress)
            # else:
            #     devAddress = " No address found."
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
           
    myList= myList.split("Your data is transferred over a secure connection")[0]         # print(hdr.text)

    context = {
        "Variable": mysummary,
        "Variable2": pkgName,
        "Variable3": variable3,
        "appImage": appImage,
        "appName": appName,
        "devName": devName,
        "text": "Downloads",
        "downloads": downloads,
        "policyURL": policyUrl,
        "address": devAddress,
         "myList": myList,
        "email": email # soup.get_text()
    }
    return context


def appStoreScrapp(url):
    global mysummary,appImage,appName ,devAddress, devName,email,pdf,downloads,policyUrl,fullLink
    mysummary,appImage,appName ,devAddress, devName,email,pdf,downloads,policyUrl,fullLink  = "","","","","","","","","",""
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
               "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers=headers)
    htmlContent = r.content

    bsoup = BeautifulSoup(htmlContent, 'html.parser')
    title = bsoup.find(
        'h1', attrs={'class': "product-header__title app-header__title"})
    # print(bsoup.get_text())
    # print(title.getText(strip=True))
    global variable3
    variable3 = "Application ID"
    # global appName
    appName = re.sub(r'\d+[+]', '', title.get_text(strip=True))
    # for h1 in bsoup.find_all('h1',attrs={'class':"product-header__titleapp-header__title"}):

    #    print(h1.get_text())
    # global devName
    devName = bsoup.find('a', attrs={'class': "link"}).getText()
    # policyUrl = bsoup.find( 'a', attrs={'class': "link icon icon-after icon-external"}).get('href')
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

                if soup.get_text():

                    # summary = ""
                    mysummary = summarize(soup.get_text(), 0.12)
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
    for tag in bsoup.find_all('a', attrs={'class': "inline-list__item"}):
        # print(tag.text)
        # global downloads
        downloads = tag.text  # This is for app store app ranking purpose
        emailregex = "\S+@\S+\.\S+"
        # global email
        email = ""
        email = re.findall(emailregex, bsoup.get_text())
        if email:
            email = email[0]
        else:
            email = "No email address found"

    # mail= mail[0].lstrip("#")
    # print(mail)
    # email=email[0].strip("-")

    context = {
        "Variable": mysummary,
        "Variable2": pkgName,
        "Variable3": variable3,
        "appImage": appImage,
        "text": "Ranking",
        "appName": appName,
        "devName": devName,
        "address": pkgName,
        "policyURL": policyUrl,
        "downloads": downloads,
        "myList": myList,
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
    print(len(summary))
    print(len(text))
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
    template_path = 'pdf.html'
    # context = {'myvar': 'this is your template context'}

    context = {
        "Variable": mysummary,
        "Variable2": devAddress,
        "Variable3": variable3,
        "appImage": appImage,
        "appName": appName,
        "devName": devName,
        "downloads": downloads,
        # "address": devAddress,
        "policyURL": policyUrl,
        "myList": myList,
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
