from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_scroller import scroll
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait





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

    #extract reviews in a csv file
    def reviews_csv(self):
        page_source = scroll(self.url) #scroll till bottom to load all the reviews
        review_url = requests.get(page_source)
        content = BeautifulSoup(review_url.text, 'html.parser')
        names_content = content.findAll('div', attrs={'class': 'RecentReviews_reviewAuthor__2W0xn'})
        comment_body = content.findAll('div', attrs={'class': 'RecentReviews_reviewComment__63GHI'})
        date_content = content.findAll('div', attrs={'class': 'RecentReviews_reviewTime___cO0n'})
        rates = content.findAll('div', attrs = {'class': 'RecentReviews_recentReviewsStars__jk_Hf'})
        
        names = []
        comment = []
        date = []
        for i,j,k in zip(names_content, comment_body, date_content):
            names.append(i.text)
            comment.append(j.text)
            date.append(k.text)
        
        ratings = []
        for i in rates:
            svgs = i.findAll('svg')
            # print(svgs)
            for svg in svgs:
                svg_id = svg.get('id')
                ratings.append(svg_id)

        interval = 5
        list_of_lists = [ratings[i:i+interval] for i in range(0, len(ratings), interval)]# create a list of all the reviews in another list

        output_list = []
        
        # push the ratings right before a recentReview_0 as the final ratings in a list  
        for sublist in list_of_lists:
            if "recentReview_0" in sublist:
                index = sublist.index("recentReview_0")
                if index > 0:
                    review = sublist[index-1].replace("recentReview_", "")
                    output_list.append(int(review))
            else:
                review = sublist[-1].replace("recentReview_", "")
                output_list.append(int(review))


        reviews_dict = {'Reviewer Name': names, 'Date': date, "Stars": output_list, "Review": comment}
        # print(len(names), len(review), len(date))
        #convert this into a dataframe
        df = pd.DataFrame.from_dict(reviews_dict, orient='index')
        prod_reviews = df.T
        prod_reviews.to_csv('reviews.csv', index=False, header=True)
