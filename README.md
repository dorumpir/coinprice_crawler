# Usage:

## 1. sync to local
git clone 
## 2. run the spiders by your requests
### A. only run one spider [please find the spider name under spiders folder]
scrapy crawl huobipro
### B. run all the spiders
scrapy crawlall
### C. schedule to run the spider services
python main.py
## 3. check the result
please find the result from mongo configured in setting.py

## Please notice, spider usdt is an exception case, so run it seperately [2.C]
python main_usdt.py