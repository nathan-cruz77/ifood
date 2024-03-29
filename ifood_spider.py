import json
import scrapy

BASE_IFOOD_URL = 'https://www.ifood.com.br/delivery/'
BASE_AVATAR_URL = 'https://static-images.ifood.com.br/image/upload/f_auto,t_high/logosgde/'
BASE_URL = 'https://marketplace.ifood.com.br/v1/merchants?latitude=-23.19529&longitude=-45.90321&channel=IFOOD'


class Restaurant(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    price_range = scrapy.Field()
    delivery_time = scrapy.Field()
    delivery_fee = scrapy.Field()
    distance = scrapy.Field()
    category = scrapy.Field()
    avatar = scrapy.Field()
    url = scrapy.Field()

    @staticmethod
    def parse_avatar(item):
        avatar = ''

        for resource in item['resources']:
            if resource['type'].lower() == 'logo':
                avatar = resource['fileName']

        if avatar:
            return ''.join([BASE_AVATAR_URL, avatar])

        return avatar


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
                'avatar': Restaurant.parse_avatar(item),
                'url': f"{BASE_IFOOD_URL}{item['slug']}/{item['id']}",
            })
