"""
1.Парсер однопоточный
2.Замер времени
3.multiprocessing Pool
4.Замер времени
5.Экспорт данных в csv
"""
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_html(url):
    responce = requests.get(url)
    return responce.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    tds = soup.find_all('tr', class_='cmc-table-row')
    links = []
    for td in tds:
        a = td.find('a', class_='cmc-link').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    
    print(len(links))
    return links    

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('div', class_='cmc-details-panel-header sc-1extin6-0 gMbCkP').find('h1').text.strip()
    except:
        name = ''
    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    except:
        price = ''

    data = {'name': name, 
            'price': price }

    return data


def write_csv(data):
    with open('coinmarket.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],
                         data['price']))

        print(data['name'], 'parsed')


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_links(get_html(url))
    for url in all_links:
        html = get_html(url)
        data = get_page_data(html)
        write_csv(data)
    
    end = datetime.now()
    total = end - start
    print(str(total))

    
if __name__ == '__main__':
    main()

