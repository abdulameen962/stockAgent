from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.linkextractors import LinkExtractor
import scrapy

class AfrinvestDivYieldSpider(scrapy.Spider):
    name = "afribank_div_yield"
    allowed_domains = ["ngxgroup.com"]