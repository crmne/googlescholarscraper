ifeq (,$(shell which python3))
	PYTHON_INTERPRETER=python
	PIP=pip
else
	PYTHON_INTERPRETER=python3
	PIP=pip3
endif

.PHONY: requirements
requirements:
	$(PIP) install -r requirements.txt

%.csv: googlescholar/spiders/googlescholar_spider.py
	FEED_FORMAT=csv scrapy crawl googlescholar -o $@

%.json: googlescholar/spiders/googlescholar_spider.py
	FEED_FORMAT=json scrapy crawl googlescholar -o $@

%.bib: %.csv
	$(PYTHON_INTERPRETER) convert_to_bibtex.py $< $@
