%.bib.csv: %.bib
	python convert.py bib2csv $< $@

%.csv: googlescholar/spiders/googlescholar_spider.py
	FEED_FORMAT=csv scrapy crawl googlescholar -o $@

%.json: googlescholar/spiders/googlescholar_spider.py
	FEED_FORMAT=json scrapy crawl googlescholar -o $@

%.bib: %.csv
	python convert.py csv2bib $< $@

