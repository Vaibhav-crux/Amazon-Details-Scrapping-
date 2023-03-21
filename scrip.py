import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

HEADERS= ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'Accept-Language': 'en-US, en;q=0.5'})

url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

items = []
for i in range(1,11):
    print('Processing {0}...'.format(url + '&page={0}'.format(i)))
    response = requests.get(url + '&page={0}'.format(i), headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    ans = soup.find_all('div', {'class': 's-result-item','data-component-type':'s-search-result'})

    for k in ans:
        product_name = k.h2.text

        try:
            rating = k.find('i',{'class':'a-icon'}).text
            reviews =k.find('span', {'class':'a-size-base s-underline-text'}).text

        except AttributeError:
            continue

        try:
            price = k.find('span', {'class':'a-price-whole'}).text
            product_url = 'https://www.amazon.in' + k.h2.a['href']
            items.append([product_url,product_name,price,rating,reviews])
        except AttributeError:
            continue

    sleep(1.5)

df = pd.DataFrame(items, columns=[' Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of reviews'])
df.to_csv("amazon_data.csv", header=True, index=False)


