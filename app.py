from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests 
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import csv
import io
import time
fro selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import urllib
import re

op=webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("disable-dev-sh-usage")

driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/Any_URL/')
def Any_URL():
    return render_template('yt_any.html')

@app.route('/Channel_Wise/')
def Channel_Wise():
    return render_template('yt_channel.html')

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        #pid = request.form.get('submit')
        searchString = request.form['content'].replace(" ","")
        filename = searchString + ".csv"
        myFile = open(filename, 'r')
        reader = csv.DictReader(myFile)
        reviews = []
        for dictionary in reader:
            reviews.append(dictionary)
        return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

@app.route('/comments',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index1():
    if request.method == 'POST':
        #if request.method == 'POST':
        co=[]
        post_id = request.form.get('submit')
        comment_yt=[]
        commenter_name=[]
        with Chrome() as driver:
            wait = WebDriverWait(driver,10)
            driver.get(post_id)

            for item in range(2): #by increasing the highest range you can get more content
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(3)
            #print(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #author-text > span"))))
            try:
                for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
                    comment_yt.append(comment.text)
                    #print(comment.text)

                for i in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #author-text > span"))):
                    #count+=1
                    commenter_name.append(i.text)
            
            except:
                return "Sorry!! Could not generate comments"
        res = {comment_yt[i]: commenter_name[i] for i in range(len(comment_yt))}
        co.append(res)
        print(co[0:(len(co)-1)])
        return render_template('results_com.html', co=co[0:(len(co))])


@app.route('/review1',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index2():
    if request.method == 'POST':
        reviews1=[]
        try:
            url = request.form['content']
            web = urllib.request.urlopen(url)
            soup1 = bs(web.read(), 'html.parser')
            data_url  = soup1.find_all("body")
            data_url1 = data_url[0].find_all("script")[21].string 
            p1 = re.compile('var ytInitialData = (.*?);')
            m1 = p1.match(data_url1)
            stocks1 = json.loads(m1.groups()[0])
        except:
            return "Not Possible to scrape"

        title=stocks1['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['title']\
            ['runs'][0]['text']
        views=stocks1['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['viewCount']\
                ['videoViewCountRenderer']['viewCount']['simpleText'][:-6]
        likes=stocks1['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']\
            ['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'].replace(' likes','')
        comment_count=stocks1['contents']['twoColumnWatchNextResults']['results']['results']['contents'][2]['itemSectionRenderer']['contents'][0]\
            ['commentsEntryPointHeaderRenderer']['commentCount']['simpleText']
        mydict = {"Video Link": url, "Title": title, "Views": views, "Likes": likes,
                          "Comment Count": comment_count}
        reviews1.append(mydict)
        print(reviews1)
        return render_template('results_any_url.html', reviews1=reviews1[0:(len(reviews1))])


@app.route('/comments1',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index3():
    if request.method == 'POST':
        #if request.method == 'POST':
        co=[]
        post_id = request.form.get('submit')
        comment_yt=[]
        commenter_name=[]
        with Chrome() as driver:
            wait = WebDriverWait(driver,10)
            driver.get(post_id)

            for item in range(2): #by increasing the highest range you can get more content
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(3)
            #print(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #author-text > span"))))
            try:
                for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
                    comment_yt.append(comment.text)
                    #print(comment.text)

                for i in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #author-text > span"))):
                    #count+=1
                    commenter_name.append(i.text)
            
            except:
                return "Sorry!! Could not generate comments"
        res = {comment_yt[i]: commenter_name[i] for i in range(len(comment_yt))}
        co.append(res)
        print(co[0:(len(co)-1)])
        return render_template('results_com.html', co=co[0:(len(co))])

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
