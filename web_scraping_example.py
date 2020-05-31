#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:50:15 2020

@author: izuchukwu
"""

import pandas as pd
import requests
import time
import logging

num_all_pages= 5027

#Initialize dataframe with require cols to hold data
data = pd.DataFrame(columns=['date','time','price','size'])
logging.info('Starting Scraping')
for page_number in range(1,num_all_pages):
    timestamp = time.time() * 1000 #multiplying by 1000 to convert to milliseconds
    timestamp = round(timestamp) #round to nearest whole number
    url = 'https://www.cmegroup.com/CmeWS/mvc/TimeandSales/133/G/M0?timeSlot=-1&pageNumber={page}&_={timestamp}'.format(
            page=page_number,timestamp=timestamp)
    r = requests.get(url)
    result = r.json()
    df = pd.DataFrame(result['entries'])
    df = df[['date','time','price','size']]
    data = data.append(df)
    logging.info('Processed {num} out of 5027. Last URL: {url}'.format(url=url,num=page_number))
    print('Processed {num} out of 5027. Last URL: {url}'.format(url=url,num=page_number))

logging.info('Final Data Cleansing')
data = data.drop_duplicates()
logging.info('Writing results to disk')
data.to_csv('Results.csv',index=False)

