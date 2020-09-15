from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
import os
from selenium import webdriver
import warnings
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import gspread
import sqlite3
from sqlite3 import Error
from oauth2client.service_account import ServiceAccountCredentials
warnings.filterwarnings("ignore")


def index(request):
    
        #driver = webdriver.Firefox(executable_path="C:\geckodriver\geckodriver.exe")
        options = Options()
        
        options.headless = True
        options.add_argument("--mute-audio")
        
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        driver.delete_all_cookies()
        

        # add sleep time here ( sec)
        sleep_time=300

        stt = time.time()
        flag=1


        kkk=0
        while True:

            # try:
                end = time.time()

                if end - stt > sleep_time or flag == 1:
                    kkk+=1
                    flag = 0
                    st = time.time()
                    # get links

                    # create chrome driver object
                    #driver = webdriver.Firefox(executable_path="C:\geckodriver\geckodriver.exe")
                    options = Options()
        
                    options.headless = True
                    options.add_argument("--mute-audio")
                    
                    prefs = {"profile.managed_default_content_settings.images": 2}
                    options.add_experimental_option("prefs", prefs)
                    driver = webdriver.Chrome(options=options)
                    driver.delete_all_cookies()

                    # get from drive links
                    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

                    creds = ServiceAccountCredentials.from_json_keyfile_name("data/creds.json", scope)

                    client = gspread.authorize(creds)

                    links = []
                    sheet = client.open("link2").sheet1  # Open the spreadhseet

                    links = sheet.col_values(1)

                    links=links[1:300]
                    # database------
                    try:
                        conn = sqlite3.connect('data/data.db')
                        cur = conn.cursor()
                    except Error as e:
                        print('database error')
                        break
                    sql =  '''insert into data_table(Url,Tags,Title,View) values (?,?,?,?)'''
                    # scrape part----
                    all_links = []
                    all_views=[]
                    all_data = []


                    count = 0
                    for link in links:
                        count += 1
                        if count%10==0:
                            driver.close()
                            # create chrome driver object
                            #driver = webdriver.Firefox(executable_path="C:\geckodriver\geckodriver.exe")
                            options = Options()
        
                            options.headless = True
                            options.add_argument("--mute-audio")
                            
                            prefs = {"profile.managed_default_content_settings.images": 2}
                            options.add_experimental_option("prefs", prefs)
                            driver = webdriver.Chrome(options=options)
                            driver.delete_all_cookies()

                        print('{} out of {}'.format(count, len(links)))
                        data = []
                        d1 = datetime.now().strftime("%d/%m/%Y")
                        data.append(d1)
                        data.append(link)
                        all_links.append(link)
                        # scrape ------------ Function
                        driver.get(link)
                        while True:
                            try:
                                temp = driver.find_element_by_class_name('super-title').text
                                break
                            except:
                                pass
                        old = 0
                        c = 0
                        # scrape------------------

                        # tags
                        try:
                            temp = driver.find_element_by_class_name('super-title').text
                            data.append(temp)
                        except:
                            data.append('')
                        # title
                        try:
                            temp = driver.find_element_by_class_name('title').text
                            data.append(temp)
                        except:
                            data.append('')

                        # view count
                        try:
                            temp = driver.find_element_by_class_name('view-count').text
                            data.append(str(temp).replace('views', '').replace(',', ''))
                            all_views.append(str(temp).replace('views', '').replace(',', ''))
                        except:
                            data.append('')
                        cur.execute(sql, (data[1],data[2],data[3],data[4]))

                        data_ = []
                        data_.append(data[1])
                        data_.append(data[4])
                        all_data.append(data_)
                    conn.commit()
                    conn.close()
                    driver.close()

                    # insert data
                    # --------------------get row part
                    d1 = datetime.now().strftime("%d/%m/%Y")


                    conn = sqlite3.connect('data/data.db')
                    cur = conn.cursor()

                    # check if need to move or not
                    sql0 = "select (date_val) from excels where date='0'"
                    cur.execute(sql0)
                    dates = cur.fetchall()
                    flag1 = 0
                    if len(dates) > 1:
                        if d1 in str(dates[0][0]):
                            flag1 = 1

                    sql1 = 'select max(date) from excels '

                    cur.execute(sql1)
                    temp = cur.fetchall()
                    max_num = temp[0]
                    try:
                        max_num = (int(max_num[0]))
                    except:
                        max_num = 1

                    # if I get the next day then
                    if flag1 == 0:
                        # move by one---
                        try:
                            # update
                            sql2 = "update excels set date=? where date=?"
                            for i in range(max_num+1, -1, -1):
                                cur.execute(sql2, (str(i + 1), str(i)))
                            conn.commit()
                        except:
                            pass

                        # insert----------
                        sql3 = "insert into excels(date,link,view,date_val) values (?,?,?,?)"
                        for dt in all_data:
                            cur.execute(sql3, ('0', dt[0], dt[1], d1))
                        conn.commit()
                    else:
                        sql_ = "delete from excels where date=0"
                        cur.execute(sql_)
                        conn.commit()

                        # insert----------
                        sql3 = "insert into excels(date,link,view,date_val) values (?,?,?,?)"
                        for dt in all_data:
                            cur.execute(sql3, ('0', dt[0], dt[1], d1))
                        conn.commit()

                    # view all [
                    all_data = []
                    cur.execute('select link from excels group by link')
                    unq_link = cur.fetchall()
                    data = []
                    links_for_all = []
                    data.append('link')
                    for link in unq_link:
                        data.append(str(link[0]))
                        links_for_all.append(str(link[0]))

                    all_data.append(data)

                    for i in range(0, max_num+1):
                        data = []
                        if i == 0:
                            data.append('Today')
                        else:
                            data.append('{} Day ago'.format(i))
                        for link in links_for_all:
                            cur.execute('select view from excels where date=? and link=?', (i, link))
                            rows = cur.fetchall()
                            try:
                                data.append(rows[0][0])
                            except:
                                data.append('')

                        all_data.append(data)


                    # get from drive links
                    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

                    creds = ServiceAccountCredentials.from_json_keyfile_name("data/creds.json", scope)

                    client = gspread.authorize(creds)

                    links = []
                    sheet = client.open("new2").sheet1  # Open the spreadhseet

                    # insert data
                    row_num = 0
                    for data in all_data:
                        row_num += 1
                        
                        c = 0
                        for dt in data:
                            c += 1
                            sheet.update_cell(c, row_num, dt)

                    print('Next Round After {} min'.format(sleep_time / 60))
            # except:
            #     print('Getting error')



        # html = "<html><body><h1 style='color:red;text-align:center;'>The Scrapping is done . Thank You.</h1></body></html>"
        # return HttpResponse(html)
        


def loadData(request):
    return render(request, "Scrape.html")