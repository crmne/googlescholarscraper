#!/usr/bin/env python
import csv
import logging

import bibtexparser
import click


@click.command(short_help=".csv -> .bib")
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def csv2bib(input_file, output_file):
    """Converts the csv INPUT_FILE to a bib OUTPUT_FILE."""
    reader = csv.reader(input_file)
    headers = next(reader) + ["ENTRYTYPE", "ID"]
    bibtex = bibtexparser.bibdatabase.BibDatabase()
    bibtex.entries = [
        dict(zip(headers, row + ["article", str(i)])) for i, row in enumerate(reader)
    ]
    output_file.write(bibtexparser.dumps(bibtex))


@click.command(short_help=".bib -> .csv")
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def bib2csv(input_file, output_file):
    """Converts the bib INPUT_FILE to a csv OUTPUT_FILE."""
    parser = bibtexparser.bparser.BibTexParser()
    bibtex = bibtexparser.load(input_file, parser=parser)

    headers = set()
    for entry in bibtex.entries:
        headers |= entry.keys()
    headers = list(headers)

    content = []
    for i, entry in enumerate(bibtex.entries):
        content.append([None] * len(headers))
        for j, key in enumerate(headers):
            content[i][j] = entry.get(key, None)

    writer = csv.writer(output_file)
    writer.writerow(headers)
    for article in content:
        writer.writerow(article)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    pass


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_lvl = logging.INFO
    logging.basicConfig(level=log_lvl, format=log_fmt)
    cli.add_command(csv2bib)
    cli.add_command(bib2csv)
    cli()
