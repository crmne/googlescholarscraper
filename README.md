GoogleScholarScraper
====================

GoogleScholarScraper is a [Scrapy][] project that implements a scraper for Google Scholar.

Features
--------

* Extracts Authors, Title, Year, Journal, and Url.
* Exports to CSV, JSON and BibTeX.
* Cookie and referer support for higher query volumes.
* Optimistically tries the next page in case of server errors.
* Supports the full Google Scholar query syntax for authors, title, exclusions, inclusions, etc. Check out those [search tips].

Installation
------------

Install Python 3.x (not tested on Python 2) and

    make requirements

Usage
-----

    export QUERY="your query here"
    export START=900  # optional: to start at page 90
    make <output filename>.csv  # or
    make <output filename>.json  # or
    make <output filename>.bib

Example
-------

    export QUERY="author:einstein quantum theory"
    unset START  # makes sure it starts from the beginning
    make einstein_quantum.bib

License
-------

GoogleScholarScraper is using the standard [BSD license](http://opensource.org/licenses/BSD-2-Clause).

[Scrapy]: https://scrapy.org/
[search tips]: http://www.otago.ac.nz/library/pdf/Google_Scholar_Tips.pdf
