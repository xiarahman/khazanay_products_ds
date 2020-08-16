from bs4 import BeautifulSoup
from requests import get
from os.path  import basename
from fake_useragent import UserAgent
import urllib.request
import pandas as pd

ua = UserAgent()

def got_soup(u):
    uag = get(u, headers={'User-Agent': ua.chrome})
    return BeautifulSoup(uag.text, 'html.parser')
    
url = 'https://www.khazanay.pk/collections/mens-casual-shoes'

page_html = got_soup(url)

products = page_html.find_all('div', itemprop='itemListElement')

all_products = []

for product in products:
    name = product.find('span', itemprop='name').text
    image_name = name.replace('/','_')
    price = product.find('span', class_='money').text
    image = product.find('img','secondary')
    src = image.get('src').replace('//','https://')
    urllib.request.urlretrieve(src, f'D:/scripts/khazanay_products_ds/images/{image_name}_image.jpg')

    product_data = [name,image_name,price]
    all_products.append(product_data)

all_products = pd.DataFrame(all_products, columns = ['name','image_name','price'])
all_products.head()
all_products.info()
all_products.to_csv(r'D:/scripts/khazanay_products_ds/products_DS.csv',index=False)
