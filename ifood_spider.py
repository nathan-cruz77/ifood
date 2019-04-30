import json
import scrapy

BASE_URL = 'https://www.ifood.com.br/marketplace/v1/merchants?latitude=-23.19529&longitude=-45.90321&channel=IFOOD'


class Restaurant(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    price_range = scrapy.Field()
    delivery_time = scrapy.Field()
    delivery_fee = scrapy.Field()
    distance = scrapy.Field()
    category = scrapy.Field()


class IfoodSpider(scrapy.Spider):
    name = 'ifood'
    start_urls = [f'{BASE_URL}&size=0']

    def parse(self, response):
        data = json.loads(response.text)

        total = data['total']
        pages_count = total // 100

        if total / 100 != total // 100:
            pages_count += 1

        for page in range(pages_count):
            yield scrapy.Request(f'{BASE_URL}&size=100&page={page}', callback=self.parse_page)

    def parse_page(self, response):
        data = json.loads(response.text)

        for item in data['merchants']:
            yield Restaurant({
                'name': item['name'],
                'rating': item['userRating'],
                'price_range': item['priceRange'],
                'delivery_time': item['deliveryTime'],
                'delivery_fee': item['deliveryFee']['value'],
                'distance': item['distance'],
                'category': item['mainCategory']['name'],
            })
