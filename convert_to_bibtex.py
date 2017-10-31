#!/usr/bin/env python
import csv
import logging

import bibtexparser
import click


@click.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def csv_to_bibtex(input_file, output_file):
    """Converts the csv INPUT_FILE to a bib OUTPUT_FILE."""
    reader = csv.reader(input_file)
    headers = next(reader) + ['ENTRYTYPE', 'ID']
    bibtex = bibtexparser.bibdatabase.BibDatabase()
    bibtex.entries = [
        dict(zip(headers, row + ['article', str(i)]))
        for i, row in enumerate(reader)
    ]
    output_file.write(bibtexparser.dumps(bibtex))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_lvl = logging.INFO
    logging.basicConfig(level=log_lvl, format=log_fmt)
    csv_to_bibtex()
