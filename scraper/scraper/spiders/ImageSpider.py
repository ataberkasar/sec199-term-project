from scrapy import Request, Spider, signals
from scrapy.exceptions import CloseSpider

from scraper.utils import *

import os
import json


class ImageSpider(Spider):
    name = "ImageSpider"
    allowed_domains = ["nitter.net"]
    
    def __init__(self, username=None, *a, **kw):
        super().__init__(*a, **kw)

        if not username:
            raise CloseSpider('Unknown Username')
        self.username = username
        self.img_dir = os.path.join('images', self.username)
        os.makedirs(self.img_dir, exist_ok=True)

    def start_requests(self):
        for request in self.helper():
            yield request

    def helper(self):
        with open(f'jsons/{self.username}_output.json', 'r', encoding='utf-8') as file:
            tweets = json.load(file)
        
        for tweet in tweets:
            tweet_date = datetime.strptime(tweet['tweet_date'], '%Y-%m-%d %H:%M:%S')
            img_url = tweet['img_url']
            
            if (img_url):
                yield Request(url=img_url, callback=self.download_img, meta={'tweet_date': tweet_date})
 
    def download_img(self, response):
        tweet_date = response.meta['tweet_date']
        img_filename = f'{tweet_date.strftime("%Y%m%d_%H%M%S")}{os.path.splitext(response.url)[1]}'
        
        img_path = os.path.join(self.img_dir, img_filename)
        with open(img_path, 'wb') as f:
            f.write(response.body)
            
