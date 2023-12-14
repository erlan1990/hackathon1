import requests
from bs4 import BeautifulSoup as bs
import lxml
import csv

def write_csv(data):
    with open('notebook.csv', 'a') as nout:
        writer = csv.writer(nout)
        writer.writerow((data['name'], data['price'], data['img']))


def get_html(url):
    response = requests.get(url).text
    return response

def get_products(html):
    soup = bs(html, 'lxml')
    products = soup.find_all('div', class_= 'row')
   
    for product in products:
        try:
            name = product.find('span', class_='prouct_name').find('a').text
        except:
            name = ''
        try:
            price = product.find('span', class_='price').text
        except:
            price = ''
        try:
            img = product.find('img').get('src')
        except:
            img = ''
       
        data={'name': name, 'price': price, 'img': img}
    
        write_csv(data)



def get_next(soup):
    pages = soup.find('div', class_= 'vm-pagination').find('ul')
    try:
        page = pages.find('li', class_='pagination-next').find('a').get('href')
        return f'https://enter.kg{page}'
    except:
        return False

def main():
    URL = 'https://enter.kg/computers/noutbuki_bishkek'
    while True:
        html = get_html(URL)
        get_products(html)
        soup = bs(html, 'lxml')
        page = get_next(soup)
        if not page:
            break
        URL = page


with open('notebook.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['name', 'price', 'img'])


main()

