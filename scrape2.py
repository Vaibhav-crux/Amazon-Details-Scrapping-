import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import csv


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'Accept-Language': 'en-US, en;q=0.5'}
items = []
with open('amazon_data.csv') as file:
        csv_reader = csv.DictReader(file)

        for csv_row in csv_reader:
                url = (csv_row['product url'])

                resp = requests.get(url, headers=HEADERS)

                s = BeautifulSoup(resp.content, features="lxml")

                des = s.select("#productTitle")[0].get_text().strip()
                details = s.select("#feature-bullets")[0].get_text().strip()

                #In given url there are 2 methods to implemented by amazon
                 # i) Required data has a class or id
                 # ii) Required data did not have any class or id

                #i)
                '''asin = s.select(".a-size-base prodDetAttrValue")[0].get_text().strip()
                manu = s.select(".a-size-base prodDetAttrValue")[0].get_text().strip()'''

                #ii)
                #worked when data not having any class or id so it founds the sibling of the data until that data found
                manufature = s.find_all('ul', {'class': 'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'})[0]
                asin = manufature.find('span', string=re.compile('ASIN')).find_next_sibling('span').text.strip()

                manu = manufature.find('span', string=re.compile('Manufacturer')).find_next_sibling('span').text.strip()
                items.append([des,asin,details,manu])

df = pd.DataFrame(items, columns=['Description','ASIN', 'Product Description', 'Manufacturer'])
df.to_csv("amazon_detail.csv", header=True, index=False)
