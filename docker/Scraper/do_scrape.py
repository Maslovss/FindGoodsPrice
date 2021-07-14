
from dataclasses import dataclass
import scrape_data
import time
import logging

import re
import requests
from bs4 import BeautifulSoup


def load_categories(soup , categories , BASE_URL):
    """Load all categories into list """

    logging.debug(f"Starting scraping categories from {BASE_URL}")
    soup = soup.find( 'div' , { 'id': 'desktop__menu' })

    category1 = ""
    category2 = ""



    for item in soup.find_all(['h4' , 'li']):

        category3 = ""
        if  item.name == "h4":
            category2 = item.find('a').text.strip() if item.find('a') is not None else "" 
            href = item.find('a')['href'] if item.find('a') is not None else "" 
            category1 = item.find_previous('div',{"class":"megadrop"}).parent.find('a').text.strip()


            if category1 != '':
                categories.append( scrape_data.Category( category1 , category2 , category2 ,  BASE_URL + href  ))
                #print(f"cat1 = {category1}| cat2 = {category2} | cat3 = {category2} | href = {BASE_URL}{href}")        

        if  item.name == "li":
            category3 = item.find('a').text.strip() if item.find('a') is not None else "" 
            href = item.find('a')['href'] if item.find('a') is not None else ""
            if href != '#':
                #print(f"cat1 = {category1}| cat2 = {category2} | cat3 = {category3} | href = {BASE_URL}{href}")
                categories.append( scrape_data.Category( category1 , category2 , category3 , BASE_URL + href  ))



def load_products(category , products ):

    logging.debug(f"Load products for category: {category.topic}=={category.subtopic}=={category.name}=={category.url}")
    this_category_products = []
    
    url = category.url 
    response = requests.get(url )
    soup = BeautifulSoup(response.text, 'lxml')

    pages = 1

    next_div = soup.find('a',{'aria-label':'Next'})
    if next_div is not None:
        next = next_div['href']
        pages = int(re.findall("(.*=)(\d+)",next)[0][1])

    print(f"Found {pages} pages")

    for i in range(1,pages+1):
        page_url = url + f'?page={i}'
        print('Load page: ' + url + f'?page={i}')
        time.sleep(0.3)
        response = requests.get(page_url )
        soup = BeautifulSoup(response.text, 'lxml')

        product_items = soup.find_all('div',{'class':'products__item'})
        for item in product_items:
            price = 0.0
            discount = 0.0
            old_price = 0.0
            product_name = ''
            product_qty = ''
            product_measure = ''
            product_div = item.find('p',{'class':'product__title'}) 
            if product_div is not None:
                product_name = product_div.find('a').text.strip()
                price_div = item.find('p',{'class':'product__price'})
                if price_div is not None:
                    discount_div = price_div.find('span',{'class':'price__discount'})
                    if discount_div is not None:
                        old_price_div = price_div.find('span',{'class':'price__old'})
                        if old_price_div is not None:
                            old_price = float(re.findall(r'\d+\.*\d*', old_price_div.text.strip())[0])
                        discount =  float(re.findall(r'\d+\.*\d*', discount_div.text.strip())[0])
                        #print(f'Discount={discount} , Old price={old_price}')
                    else:
                        price = float(re.findall(r'\d+\.*\d*', price_div.find('b').text.strip())[0])
                        #print(f'Price={price:.2f}')

                r = re.findall(r'\d+\,*\d*\s(?:л|г|кг|мл|мг|шт\.)(?:\s|$)',product_name)
                if len(r)>0:
                    product_qty_measure =r[0]
                    product_qty = re.findall(r'\d+\,*\d*',product_qty_measure)[0]
                    product_measure =  re.findall(r'(?:л|г|кг|мл|мг|шт\.)',product_qty_measure)[0]
                del r

                this_category_products.append( scrape_data.Product(  category.topic , category.subtopic , category.name , \
                                                   product_name , '0' ,product_qty , product_measure , \
                                                   price , discount , old_price 
                                                   )  
                            )

    logging.debug(f"Write {len(this_category_products)} products into database")
    scrape_data.write_products(this_category_products,"Tavriav")
    products.append(this_category_products)




######################################


def main():


    #init logger  etc
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )


    BASE_URL = 'https://www.tavriav.ua'

    t0 = time.time()
    logging.debug(f"Main scraping from {BASE_URL}")


    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'lxml')

    categories = []

    load_categories(soup , categories , BASE_URL)

    categories = categories[2:]
    new_categories = []

    old_cat1 , old_cat2 , old_cat3 = "init" , "init" , "init"
    
    # Надо из списка categories убрать ссылки на всю категорию, для которой существуют подкатегории
    # для того, чтобы не загружать товары два раза: сналача по старице субкатегории все товары, 
    # а потом еще раз из подкатегории те же товары 
    for i in range(0,len(categories)-1):
        if not ( categories[i].subtopic == categories[i].name and categories[i+1].subtopic == categories[i].subtopic):
            new_categories.append(categories[i])
        old_cat1 , old_cat2 , old_cat3 = categories[i].topic , categories[i].subtopic, categories[i].name
    new_categories.append(categories[-1])
    categories = new_categories

    scrape_data.create_tables()

    products = []
    #for category in categories[40:53]:
    for category in categories:
        load_products(category , products )

    for item in categories:
        pass
        #print(item)

    t_delta = time.time() - t0
    logging.debug(f"Done in {t_delta} seconds")
    print(f"Done in {t_delta} seconds")

if __name__ == "__main__":
    main()
