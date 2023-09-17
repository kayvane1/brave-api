# :toolbox: Getting started

This project uses [Poetry](https://python-poetry.org/) for dependency management. To start developing here, you need to install Poetry

* Follow the instructions on the [official docs](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

Once you have Poetry installed on your system simply run:

```bash
poetry install
```

This will create a virtual environment and install the required dependencies.

:blue_book: For more information on how to use poetry, either check our [Notion](https://www.notion.so/util-km/Using-Python-Poetry-94f420f6008d48e690a712a8f91c8870) for a quick guide, or read the [official docs.](https://python-poetry.org/docs/master/)

## :building_construction: Setting up your local environment

Simply run the following make command to create a virtual environment and start developing:

```bash
make init
```

This will clean up your current virtual env, install poetry, create a new virtual environment and install all dependencies for you.

You can use the following step to activate your newly createdvirtualenv.

```bash
source .venv/bin/activate
```

To add/remove dependencies just use Poetry cli! Like this:

```bash
poetry add requests
```

## :notebook: Useful commands

* `make help`       To get a list of ready to use recipes
* `poetry list`     Lists all available Poetry commands
