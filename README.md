# Brave Search API

## Overview
Python wrapper for the [Brave Search API](https://search.brave.com/api).

Brave Search doesn’t track you or your queries, it's a privacy-preserving alternative to Google Search. It offers many endpoints for developers to build on top of. This module is a wrapper for the Brave Search API.

Notes:
- This repo is under active development and is not yet ready for production use.
- Pypi is currently not accepting new registrations, so this package is not yet available on Pypi. Once Pypi is accepting new registrations, this package will be available on Pypi.

## Usage

The module supports both synchronous and asynchronous requests. Your Brave API key can either be passed as an environment variable under `BRAVE_API_KEY` or as an argument to the Brave class.

```python

from brave import Brave

brave = Brave()

query = "cobalt mining"
num_results = 10

search_results = brave.search(q=query, count=num_results)

```

The module also supports asynchronous requests:

```python

from brave import AsyncBrave

brave = AsyncBrave()

query = "cobalt mining"
num_results = 10

results = await brave.search(q=query, goggles_id=goggle_url, count=num_results, result_filter=result_filter)
```
## Features

### Download PDFs:

    ```python
    from brave import Brave

    brave = Brave()

    query = "cobalt mining"
    num_results = 10

    search_results = brave.search(q=query, count=num_results)

    search_results.download_pdfs()
    ```

### Aggregate Price Data

```python

    from brave import Brave

    brave = Brave()

    query = "Blue Tack"
    num_results = 10
    country = "US"
    search_results = brave.search(q=query, count=num_results, country=country)
    print(search_results.product_prices())
    # >> [6.28, 5.98, 4.99, 13.18, 6.59, 7.8, 5.56, 10.79, 5.02, 10.56, 16.95, 9.99, 23.59, 16.31, 11.96]
    print(search_results.product_price_ranges())
    # >> (4.99, 23.59)
```

### Aggregate Review Data

```python

from brave import Brave

brave = Brave()

query = "Blue Tack"
num_results = 10
search_results = brave.search(q=query, count=num_results)
print(search_results.average_product_review_score())
# >> 88.13333333333333

```

### Goggles

Brave is a powerful search engine that allows for the usage of `goggles` to rerank your search results to meet your use-case. [Goggles](https://search.brave.com/help/goggles) enable any individual—or community of people—to alter the ranking of Brave Search by using a set of instructions (rules and filters). Anyone can create, apply, or extend a Goggle. Essentially Goggles act as a custom re-ranking on top of the Brave search index.

Here we use a goggle which prioritizes academic and archival sources.

```python

from brave import Brave

query = "cobalt mining"
goggle_url = "https://raw.githubusercontent.com/CSamuelAnderson/Brave-goggles/main/academic-and-archival.goggle"
num_results = 10
result_filter = "web" # must be comma separated string

results = brave.search(q=query, goggles_id=goggle_url, count=num_results, result_filter=result_filter)

```

## Installation

This package uses Poetry for dependency management. To start developing here, you need to install Poetry

* Follow the instructions on the [official docs](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

Once you have Poetry installed on your system simply run:

```bash
make init
```

## Developing

Check the [CONTRIBUTING.md](/CONTRIBUTING.md) for information about how to develop on this project.
