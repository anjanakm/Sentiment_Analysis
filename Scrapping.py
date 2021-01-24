import requests 
from bs4 import BeautifulSoup
import sqlite3
import csv_to_sqlite 
from time import sleep
from selenium import webdriver
#import time
#import random as rand 
import sqlite3 as sql
import pandas as pd



 #Remember to update the number of pages 

review_dict = {'review':[]}


    #time.sleep(rand.randint(3,30)) 
url = 'https://www.etsy.com/in-en/listing/546737718/star-ear-crawler-earrings-925-sterling?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-8&bes=1' 
browser = webdriver.Chrome(executable_path="D:\chromedriver")
browser.get(url)
user_agent = {'User-agent': 'Chrome'}
response = requests.get(url, headers = user_agent)

soup = BeautifulSoup(response.text, 'html.parser')


for i in range(1,51):
    try:
        
        for r in range(4):
            h= browser.find_element_by_xpath('//*[@id="review-preview-toggle-' +str(r)+'"]').text
            review_dict['review'].append(h)
    except:
        pass
        

   
       
    next_1 = browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a')
    next_1.click()
   
    sleep(4)
  
        
        
reviews = pd.DataFrame(review_dict)
reviews.to_csv(r'C:\Users\user\OneDrive\Desktop\reviews.csv', index=False) 


conn = sql.connect('etsy_reviews.db')

reviews.to_sql('REVIEWS', conn)


#load the database table back to dataframe
conn = sql.connect('etsy_reviews.db')
new_df = pd.read_sql('SELECT * FROM REVIEWS ',conn)
new_df.to_csv(r'C:\Users\user\OneDrive\Desktop\Forskcoding-Data Science\reviews_etsy.csv', index=False) 
print(new_df.sample(5))