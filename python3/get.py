#!/root/anaconda3/bin python

import os

# Linux Python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Encoding Checker
#print(sys.getdefaultencoding())
#print(sys.stdout.encoding)

# Scrapy
import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

error_urls = []

import time
import random

import pickle
import codecs
import re, pprint

import sys
sys.path.append('./mysite')
from mysite import wsgi
from nutrition.models import Item, Composition, Nutrition


def error_detect(fn, soup):
  try:
    return fn(soup)
  except Exception as e:
    print("error ", e)
    return u"No Data"

def output_pickle(dic, filename):
  output = open(filename +'.pkl', 'w')
  pickle.dump(dic, output)
  output.close()

def extract_unit(x):
  string = str(x).split()
  temp_string = ""
  try:
    for x in string[0]:
      if x != ",":
        temp_string += x
  except:
    pass

  if len(string) > 1:
    temp_unit = string[1]
  else:
    temp_unit = "no_value"
  return temp_string, temp_unit

def pp(obj):
  pp = pprint.PrettyPrinter(indent=4, width=160)
  str = pp.pformat(obj)
  return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

def load_pickle(filename):
  pkl_file = open("Supplements.pkl")
  data1 = pickle.load(pkl_file)
  print(pp(data1))
  pkl_file.close()

def return_soup(url):
  from bs4 import BeautifulSoup as bs
  import requests
  res = requests.get(url)
  soup = bs(res.content, "html.parser")
  return soup


def get_product_url(url):
  soup = return_soup(url)
  results = soup.select("div.ga-product a.link-overlay")
  arr = []
  for result in results:
    url = result.get("href")
    arr.append(url)
  return arr

class Spider(scrapy.Spider):
  name = 'items'
  start = int(os.getenv('SCRAPY_START_INDEX', 22419))
  target_range = int(os.getenv('SCRAPY_NUM_ITEMS', 1000))
  start_urls = ['https://www.iherb.com/pr/pr/' + str(x) for x in range(start, start + target_range) ]    

  def parse(self, response):
    time.sleep(random.randint(2, 3))

    product_url = response.url
    self.logger.info('url=%s', product_url)

    sel = Selector(response)

    supplement = sel.xpath('//*[@id="breadCrumbs"]/a[4]/text()').extract_first()
    if supplement != 'サプリメント':
      return

    product_name = error_detect(self.get_product_name, response)

    company = error_detect(self.get_company, response)
    amount = error_detect(self.get_amount, response)
    capsule_type = error_detect(self.get_capsule_type, response)
    rating_count = error_detect(self.get_rating_count, response)
    rating = error_detect(self.get_rating, response)
    price = error_detect(self.get_price, response)
    product_code = error_detect(self.get_product_code, response)
    serving_size = error_detect(self.get_serving_size, response)
    nutrition = error_detect(self.get_nutrition, response)


    dic = self.gen_dic(product_name, product_url, company, amount, capsule_type, rating_count, rating, price, product_code, serving_size, nutrition)

    self.logger.info('dic=%s', dic)
    
    self.output_db(dic)

  def get_product_name(self, sel):
    product_name = sel.xpath('//*[@id="name"]/text()').extract_first()
    self.logger.info('product_name = %s', product_name)
    return product_name

  def get_company(self, sel):
    company = sel.xpath('//*[@id="brand"]/a/span/bdi/text()').extract_first()
    self.logger.info('company = %s', company)
    return company
  
  import re
  def get_amount(self, sel):
    amount = sel.xpath('//*[@id="product-specs-list"]/li[5]/text()').re_first(r'内容量:\s\s\s(\d+)')
    self.logger.info('amount = %s', str(amount))
    return amount

  def get_capsule_type(self, sel):

    pre_string  = sel.xpath('//*[@id="product-specs-list"]/li[5]/text()').extract_first()
    self.logger.info('capsule_type = %s', pre_string)
    out = 'no value'
    pattern = r'内容量:\s\s\s\d+\s'
    repattern = re.compile(pattern)
    mh = repattern.match(str(pre_string))
    if mh:
      out = pre_string[mh.end()+1:]
    self.logger.info('capsule_type = %s', out)
    return out

  def get_rating_count(self, sel):
    rating_count = sel.xpath('/html/head/meta[12][contains(@property, "og:rating_count")]/@content').extract_first()
    self.logger.info('rating_count = %s', rating_count)
    return rating_count
  
  def get_rating(self, sel):
    rating = sel.xpath('/html/head/meta[10][contains(@property, "og:rating")]/@content').extract_first()
    self.logger.info('rating = %s', rating)
    return rating
  
  def get_price(self, sel):
    price = sel.xpath('/html/head/meta[4][contains(@property, "og:price:amount")]/@content').extract_first()
    self.logger.info('price = %s', price)
    for x in price:
      if x != ",":
        temp_price += x
  
    temp_price = temp_price.replace(" ", "")
    return temp_price
  
  
  def get_product_code(self, sel):
    product_code = sel.xpath('//*[@id="product-specs-list"]/li[3]/span/text()').extract_first()
    self.logger.info('product_code = %s', product_code)
    return product_code
  
  def get_serving_size(self, sel):
    pre_string = sel.xpath('//*[@class="supplement-facts-container"]/table/tr[2]/td/text()').re_first(r'\s(\d+)\s')
    self.logger.info('serving_size (out) = %s', pre_string)
    if isinstance(pre_string,type(None)):
      serving_size = sel.xpath('//*[@class="supplement-facts-container"]/table/tbody/tr[2]/td/text()').extract_first().re(r'\s\d+\s')
    if isinstance(pre_string,type(None)):
      return "no value"
    return pre_string


    serving_size = serving_size.strip()
    self.logger.info('serving_size = %s', serving_size)
    return serving_size
    str_serving_size = [str(x).lower() for x in serving_size]
    for x in str_serving_size:
      if "serving size" in x:
        y = x.split()[3]
        if "</strong>" in y:
          y.replace('</strong>', '')
        return y
    return "no value"
  
  
  def get_nutrition(self, sel):
    nut = []
    x = 1
    raw_nutrition = sel.xpath('//div[@class="supplement-facts-container"]/table/tr')
    if isinstance(raw_nutrition,type(None)):
      raw_nutrition = sel.xpath('//div[@class="supplement-facts-container"]/table/tbody/tr')
    if isinstance(raw_nutrition,type(None)):
      return []
    for i, n in enumerate(raw_nutrition.extract()):
      if isinstance(raw_nutrition.xpath('//tr[' + str(i+4) + ']/td[1]/text()').extract_first(), type(None)):
        break
      each_nutrition = raw_nutrition.xpath('//tr[' + str(i+4) + ']/td[1]/text()').extract_first()
      each_amount = raw_nutrition.xpath('//tr[' + str(i+4) + ']/td[2]/text()').extract_first()
      dvc = raw_nutrition.xpath('//tr[' + str(i+4) + ']/td[3]/text()').extract_first()
      dva = raw_nutrition.xpath('//tr[' + str(i+4) + ']/td[4]/text()').extract_first()
      amount, unit = extract_unit(each_amount)
      dic = {
        "each_nutrition": each_nutrition,
        "each_amount": amount,
        "each_unit": unit
      }
      self.logger.info('dic = %s',dic)
      nut.append(dic)
    return nut 

  
  def gen_dic(self, *args):

    dic = {
      "product": args[0],
      "url": args[1],
      "company": args[2],
      "amount": args[3],
      "capsule_type": args[4],
      "rating_count": args[5],
      "rating": args[6],
      "price": args[7],
      "product_code": args[8],
      "serving_size": args[9],
      "nutrition": args[10],
    }
    return dic

  import pprint
  def output_db(self, dic):
    pp = pprint.PrettyPrinter(indent=4)
  
    nutritions = []

    item = Item()
    item.product_name = dic['product']
    item.product_url = dic['url']
    item.company = dic['company']
    item.amount = dic['amount']
    item.capsule_type = dic['capsule_type']
    item.rating_count = dic['rating_count']
    if dic['rating'] != None:
      item.rating = dic['rating']
    else:
      item.rating = 0.0
    

    try:
      price = float(dic['price'])
      item.price = price
    except:
      item.price = None

    item.product_code = dic['product_code']
    try:
      serving_size = int(dic['serving_size'])
      item.serving_size = serving_size
    except:
      item.serving_size = 1
    item.save()
    pp.pprint(item.id)
  
    for x in range(len(dic['nutrition'])):
      try:
        nut = Nutrition.objects.filter(name=str(dic['nutrition'][x]['each_nutrition']))
      except:
        nut = []
      print('nut=',nut) 
  
      composition = Composition()
      if len(nut) == 0:
        nutrition = Nutrition()
        try:
            nname = str(dic['nutrition'][x]['each_nutrition'])
            nutrition.name = nname
        except:
          nutrition.name = ''
        nutrition.save()
  
        composition.name = nutrition
      else:
        composition.name = nut[0]
      
      try:
        amount = int(dic['nutrition'][x]['each_amount'])
        composition.amount = amount
      except:
        composition.amount = 0
      try:
        unit = str(dic['nutrition'][x]['each_unit'])
        composition.unit = unit
      except:
        composition.unit = ''
      
      composition.save()
      item.composition.add(composition)
    item.save()



class ScrapySettings:
    Common =   {
      'BOT_NAME':'stand-alone',
      'HTTPERROR_ALLOWED_CODES':'True',
      'DEFAULT_REQUEST_HEADERS':{
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en',
          'User-Agents':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                              },
      #'USER_AGENT':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 
      'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
      #'REDIRECT_ENABLED':'False',
      'scrapy.telnet.TelnetConsole': None,
      'CONCURRENT_ITEMS': os.getenv('SCRAPY_CONCURRENT_ITEMS', '10000'),
      'CONCURRENT_REQUESTS':os.getenv('SCRAPY_CONCURRENT_REQUESTS', '10000'),
      'DOWNLOAD_DELAY' : float(os.getenv('SCRAPY_DOWNLOAD_DELAY', 0.0)),
    }



def spy_items(target_range):
    url_list = ['https://www.iherb.com/pr/pr/' + str(x) for x in range(target_range) ]
    
    SS = ScrapySettings()
    configure_logging()
    runner = CrawlerRunner(Settings(values=SS.Common, priority='project'))

    runner.crawl(Spider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()

    return 

if __name__ == "__main__":
  spy_items(10)

