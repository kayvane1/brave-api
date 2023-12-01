# Brave Search API

## Overview
Python wrapper for the [Brave Search API](https://search.brave.com/api). Currently implements the web search endpoint, further endpoints will be added in the future.

## Usage

```python

from brave import Brave

brave = Brave()

query = "cobalt mining"
goggle_url = "https://raw.githubusercontent.com/CSamuelAnderson/Brave-goggles/main/academic-and-archival.goggle"
num_results = 10
result_filter = "web" # must be comma separated string

results = brave.search(q=query, goggles_id=goggle_url, count=num_results, result_filter=result_filter)

results.download_all_pdfs(path="downloads")

```

The module also supports asynchronous requests:

```python

from brave import AsyncBrave

brave = AsyncBrave()

query = "cobalt mining"
goggle_url = "https://raw.githubusercontent.com/CSamuelAnderson/Brave-goggles/main/academic-and-archival.goggle"
num_results = 10
result_filter = "web" # must be comma separated string

results = await brave.search(q=query, goggles_id=goggle_url, count=num_results, result_filter=result_filter)

results.download_all_pdfs(path="downloads")

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
