from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

from scraper.utils import *

import os


class NitterSpider(CrawlSpider):
    name = "NitterSpider"
    allowed_domains = ["nitter.net"]
    
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css='div.show-more a:contains("Load more")'), callback='parse', follow=True),
    )
    
    def __init__(self, username=None, _from=None, img_dir=None, *a, **kw):
        super().__init__(*a, **kw)
        
        if not username:
            raise CloseSpider('Unknown Username')
        
        self.start_urls = [f"https://nitter.net/{username}"]
        self.username = username
        self._from = time_before(_from) if _from else None
        
        os.makedirs('jsons', exist_ok=True)
        

    def parse_start_url(self, response):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        
        for tweet in response.css('.timeline-item'):
            if tweet.css('.show-more'):
                continue
            if tweet.css('.pinned'):
                continue
            if tweet.css('.retweet-header'):
                continue
            
            tweet_date_str = tweet.css('.tweet-date a::attr(title)').get()
            tweet_date = get_datetime(tweet_date_str)
            
            if (self._from and tweet_date < self._from):
                raise CloseSpider('Max Time Interval Reached')

            tweet_text = ''.join(tweet.css('.tweet-content *::text').getall())
            relative_url = tweet.css('.still-image::attr(href)').get()
            img_url = response.urljoin(relative_url)  if relative_url else None
            
            
            # if (img_url):
            #     yield Request(url=img_url, callback=self.download_img, meta={'tweet_date': tweet_date})

            yield {
                'tweet_date': tweet_date,
                'tweet': tweet_text,
                'img_url': img_url
            }
    
    def download_img(self, response):
        tweet_date = response.meta['tweet_date']
        img_filename = f'{tweet_date.strftime("%Y%m%d_%H%M%S.jpg")}'
        img_path = os.path.join(self.img_dir, img_filename)
        with open(img_path, 'wb') as f:
            f.write(response.body)
            
