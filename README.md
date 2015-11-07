# webscraper-python
Sample web scraping with Python3

## Setup on Mac OS

```bash
$ brew install pyenv

$ xcode-select --install

$ pyenv install 3.5.0

$ pip install beautifulsoup4 pyyaml
```

## Configure

```bash
$ mv config.yml.sample config.yml

$ vim config.yml
```

## Run

```bash
$ pyenv local 3.5.0

$ cd webscraper-python
$ ./scraper.py
```
