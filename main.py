from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(self, url):
        self.url = url
        self.content = None

    def get_content(self):
        response = requests.get(self.url)
        self.content = BeautifulSoup(response.text, 'html.parser')

    def get_price(self):
        response = requests.get(self.url)
        content = BeautifulSoup(response.text, 'html.parser')
        for div in content.findAll('div', attrs={'class':'ProductPriceContainer_mrp__mDowM'}):
            return div.text


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

#reviews
    def reviews_csv(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        chromedriver_path = "C:/Users/salwy/Downloads/chromedriver_win32/chromedriver.exe"

        driver = webdriver.Chrome("C:/Users/salwy/Downloads/chromedriver_win32/chromedriver.exe", options)
        driver.get(self.url + "/reviews")
        time.sleep(3)

        while True:
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(2)  # Wait for the page to load new reviews

            last_review = driver.find_elements_by_class_name("RecentReviews_noMoreReviews__1Cx2F")
            if last_review:
                break

        page_source = driver.page_source
        driver.quit()

        review_url = requests.get(page_source + "/reviews")
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
        # for i in range(len(ratings)):
        #     if ratings[i] == 'recentReview_0':
        #         print(ratings[i-1])
        interval = 5
        list_of_lists = [ratings[i:i+interval] for i in range(0, len(ratings), interval)]

        output_list = []

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
        df = pd.DataFrame.from_dict(reviews_dict, orient='index')
        prod_reviews = df.T
        prod_reviews.to_csv('reviews.csv', index=False, header=True)
