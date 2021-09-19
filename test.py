from browser import Browser
from posmark import Poskmark
from functions import get_category_dict
import requests


class SaleProduct(object):
    def __init__(self, blob_list: list, title, description, category: list, size, original_price, listing_price):
        self.blob_list = blob_list
        self.title = title
        self.description = description
        self.category = category
        self.size = size
        self.original_price = original_price
        self.listing_price = listing_price


if __name__ == '__main__':

    sale_product_data = {
        "blob_list": [
            'E:/code/poshmark_test/data/image/1/1.jpg',
            'E:/code/poshmark_test/data/image/1/2.jpg',
            'E:/code/poshmark_test/data/image/1/3.jpg',
            'E:/code/poshmark_test/data/image/1/4.jpg',
        ],
        "title": "Males children wear",
        "description": "Males children wear 2021 ",
        "category": ["Kids", "Swim", 'Coverups'],
        "size": ["Boys", "7"],
        "original_price": 100,
        "listing_price": 60,
    }
    category_dict = get_category_dict()
    sale_product = SaleProduct(**sale_product_data)
    browser = Browser("127.0.0.1", port=35000, profile_id="3A4D1C87-7F63-474E-BADA-416F6BD9A3FF",
                      chrome_driver="./chromedriver.exe")
    page = Poskmark(browser, sale_product, category_dict)
    page.execute()
    print('1')
