items.csv: googlescholar/spiders/googlescholar_spider.py
	FEED_FORMAT=csv scrapy crawl googlescholar -o items.csv

items.json: googlescholar/spiders/googlescholar_spider.py
	FEED_FORMAT=json scrapy crawl googlescholar -o items.json
