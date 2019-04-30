# Ifood Crawler
Fetches restaurants that deliver via ifood in a given location. Change the zip code
or location on the spider `start_url` to get results from somewhere
else.

## Installation
If you are using `pipenv` simply run:

```shell
$ pipenv install
```

You may also use `pip`:

```shell
$ pip install -r requirements.txt
```

## Running
To run the spider use:

```shell
$ scrapy runspider ifood_spider.py -o restaurantes.csv
```

You may also use any other output format already supported by scrapy.
See [here](https://docs.scrapy.org/en/latest/topics/feed-exports.html#serialization-formats).
