from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlparse
import json

def get_productID(url):
    parsed_url = urlparse(url)

# Extract the path from the URL
    path = parsed_url.path

# Split the path by '-'
    path_parts = path.split('-')

# Get the last part of the path (product ID)
    product_id = path_parts[-1]

    return product_id


def get_reviews(url):
    api_url= f"https://pharmeasy.in/api/browse/product/reviews/{get_productID(url)}?page=1&showAll=1"
    response = requests.get(api_url)
    data_json = json.loads(response.content)
    i = 1

    while(len(data_json['data']['response'])!=0):
        api_url= f"https://pharmeasy.in/api/browse/product/reviews/{get_productID(url)}?page={i}&showAll=1"
        response = requests.get(api_url)
        data_json = json.loads(response.content)
        reviews_dict = data_json['data']['response']    
        df = pd.DataFrame(reviews_dict)
        df.to_csv('reviews.csv', index=False, header=(i == 1), mode='a')
        i+=1
