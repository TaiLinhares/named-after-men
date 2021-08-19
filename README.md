# Named after Men - Daily post bot

## Description

Queries and formats content from a Postgresql database and posts it on Twitter and on a Wordpress blog. If the code throws any exception, the maintainer is notified per email.

## Context

This repository is part of the data/art project **Named after Men**, which posts daily on Twitter and on the website [namedaftermen.com](www.namedaftermen.com) a plant that was named after a male botanist. The goal of this project is to reflect on the power structures that regulate the act of naming.

## Setup

### Handling secrets and environment variables

Copy the `.env.template` file and rename it to `.env` add your secrets here. These values will then be loaded as environment variables and used to create a config object in the config package.

### Set virtual environment

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
https://docs.python.org/3/tutorial/venv.html

#### On VS Code using Conda as interpreter

```sh
conda activate base
```

#### Create virtual environment on the project root folder

```sh
python -m venv venv
```

#### Activate virtual environment

```sh
venv\Scripts\activate
// or on linux
source venv/bin/activate
```

#### Deactivate virtual environment

```sh
deactivate
```

#### Useful Python commands

```sh
// Check version, installed packages, and current environment
py --version
py -m  pip list
where python

// If virtualenv package not installed
py -m pip install virtualenv

// Update requirements.txt
pip3 freeze > requirements.txt
```

### Pythonic Linting

This project is linted using both [Black](https://pypi.org/project/black/) and [Pycodestyle(https://pypi.org/project/pycodestyle/). Both can be installed locally and ran with the following commands.

```sh
black .
pycodestyle .
```

Configuration for pycodestyle can be found in the `./setup.cfg` file. The linters will also run as github actions when code is pushed to Github.


### Running locally vs. running on Heroku

The `FileSystemLoader` template path parameter starts on the root folder on Heroku `src/templates`, while it starts from the src folder when running locally, that is `templates`.