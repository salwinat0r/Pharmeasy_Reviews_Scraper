from fastapi import FastAPI
from main import Scraper
from pydantic import BaseModel
app = FastAPI(title="Pharmeasy Scraper")

# @app.get("/")
# def root():
#     return {"Hello": "World"}
class ProductURL(BaseModel):
    url: str


@app.post("/url")
def get_reviews(product_url: ProductURL):
    url = product_url.url
    product = Scraper(url)
    product.get_content()

    price = product.get_price()
    rating = product.get_rating()
    reviews = product.get_reviews()
    productID = product.get_productID()

    result = {
        "price": price,
        "rating" : rating,
        "reviews" : "The reviews are converted inserted in the csv file"
    }
    return result

