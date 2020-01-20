
# Scrap2DB Docker Service Example

Scraping web site to save to DB in Docker

This sample uses [iHerb](https://www.iherb.com/) as target site.


### Main Dependency

- Docker

- Docker Compose

- MariaDB

- Python

- Django

- Scrapy


### Installation

  ```
  docker-compose up -d --build
  ```

### Run

  ```
  ./start.sh
  ```

### Access to DB by Django Admin

http://localhost/admin


Default user is
```
USERNAME: root
PASSWORD: initpass
```

### Access to DB

http://localhost/admin

### Configuration

Specify Environmental Valiable by docker-compose for Scrapy Configuration following

- SCRAPY_START_INDEX: 22419
- SCRAPY_NUM_ITEMS: 1000
- SCRAPY_CONCURRENT_ITEMS: 10000
- SCRAPY_CONCURRENT_REQUESTS: 2
- SCRAPY_DOWNLOAD_DELAY: 8.0
