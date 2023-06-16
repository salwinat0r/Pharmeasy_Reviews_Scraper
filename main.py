from bs4 import BeautifulSoup
import requests
import pandas as pd

main_url = 'https://pharmeasy.in/health-care/products/everherb-karela-jamun-juice---helps-maintains-healthy-sugar-levels--helps-in-weight-management---1l--501050'
url = requests.get(main_url)
content = BeautifulSoup(url.text, 'html.parser')


def price(content):
    for div in content.findAll('div', attrs={'class':'ProductPriceContainer_mrp__mDowM'}):
        print(div.text)

def ratings(content):
    div = content.find('div', class_='OverviewSection_starsDiv___fLfB')
    svgs = div.findAll('svg')
    ratings = []
    for svg in svgs:
        svg_id = svg.get('id')
        ratings.append(svg_id.split("_"))
    return float(ratings[len(ratings)-1][1]) + float(ratings[len(ratings)-2][1])


#reviews
review_url = requests.get((main_url + '/reviews'))
review_content = BeautifulSoup(review_url.text, 'html.parser')

def reviews(content):
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




    

print(reviews(review_content))