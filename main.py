from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.parse import urlparse
import json





class Scraper:
    def __init__(self, url):
        self.url = url
        self.content = None

    def get_content(self):
        response = requests.get(self.url)
        self.content = BeautifulSoup(response.text, 'html.parser')

    #retrieve price of the product
    def get_price(self):
        response = requests.get(self.url)
        content = BeautifulSoup(response.text, 'html.parser')
        for div in content.findAll('div', attrs={'class':'ProductPriceContainer_mrp__mDowM'}):
            return div.text

    #retrieve ratings given to the product
    def get_rating(self):
        response = requests.get(self.url)
        content = BeautifulSoup(response.text, 'html.parser')
        div = content.find('div', class_='OverviewSection_starsDiv___fLfB')
        svgs = div.findAll('svg')
        ratings = []
        for svg in svgs:
            svg_id = svg.get('id')
            ratings.append(svg_id.split("_"))
        return float(ratings[len(ratings)-1][1]) + float(ratings[len(ratings)-2][1])

    def get_productID(self):
        parsed_url = urlparse(self.url)
    # Extract the path from the URL
        path = parsed_url.path
    # Split the path by '-'
        path_parts = path.split('-')
    # Get the last part of the path (product ID)
        product_id = path_parts[-1]

        return product_id

    def get_reviews(self):
        """
        Use the Pharmeasy API to extract reviews into a csv file.
        """
        api_url= f"https://pharmeasy.in/api/browse/product/reviews/{self.get_productID()}?page=1&showAll=1"
        response = requests.get(api_url)
        data_json = json.loads(response.content)
        i = 1

        while(len(data_json['data']['response'])!=0):
            api_url= f"https://pharmeasy.in/api/browse/product/reviews/{self.get_productID()}?page={i}&showAll=1"
            response = requests.get(api_url)
            data_json = json.loads(response.content)
            reviews_dict = data_json['data']['response']    
            df = pd.DataFrame(reviews_dict)
            df.to_csv('reviews.csv', index=False, header=(i == 1), mode='a')
            i+=1