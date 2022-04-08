import csv
import requests
from bs4 import BeautifulSoup

def get_html(url):
    respons = requests.get(url)
    return respons.text
    
def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages_ul = soup.find('div',class_='pager i-pager pagination').find('div')
    last_page = pages_ul.find_all('a')[-1]
    total_pages = last_page.get('href').split('=')[-1]
    return int(total_pages)

def write_to_csv(data):
    with open ('wildberries.csv','w') as file:
        writer = csv.writer(file, delimiter='/')
        writer.writerow((data['title'],data['title1'],data['price'],data['']))

def get_page_data(html):
    soup = BeautifulSoup(html,'html.parser')
    try:
    
        product_list = soup.find('div','catalog-page__main new-size').find('div','catalog-page__content').find('div','product-card-list')
        products = product_list.find_all('div','product-card__wrapper')
    
    
    
        for product in products:
            try:
                photo = product.find('div',class_='product-card__img').find('img').get('src')
            except:
                photo =''

            try:
                title = product.find('div',class_='product-card__brand-name').find('span',class_='goods-name').text
            except:
                title=''

            try:
                title1 = product.find('div',class_='product-card__brand-name').find('strong').text
            except:
                title=''

            try:
                price = product.find('div',class_='product-card__price j-cataloger-price').find('ins').text
            except:
                price = ''

        
        data = {'title': title,'title1':title1,'price': price,'photo':photo}
    
    except AttributeError:
        print(html)
            


def is_disableb(html):
    soup = BeautifulSoup(html,'lxml')
    pages_ul = soup.find('div',class_='pager i-pager pagination').find('div')
    last_page = pages_ul.find_all('a')[-1]
    total_pages = last_page.get('href').split('=')[-1]
    if 'disabled' in total_pages.get('class'):
        return True
    return False

def main():
    obuv_url = 'https://kg.wildberries.ru/catalog/obuv/zhenskaya?sort=popular&cardsize=c516x688&page'
    pages = '='
    total_pages = get_total_pages(get_html(obuv_url))
    for page in range(1, total_pages+9999999):
        url_with_page = obuv_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)
main()