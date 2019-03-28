# -*- coding: utf-8 -*-
import scrapy
import csv
import os


class ReifenSpider(scrapy.Spider):
    name = 'reifen' #Spider Name
    allowed_domains = ['reifen.de']
    start_urls = []


    #It's read the all row for GTIN
    # with open('Input/gtin.csv', 'r') as f:
    with open(os.path.join("Input","gtin.csv"), 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            line=line[0].strip()
            # .format to making ready to requests
            links='https://www.reifen.de/reifen/offroad_suv_4x4/andere?freeTextSearch=true&text={}&sort=popularity'.format(line)
            
            start_urls.append(links) #finally appened to start_urls


    # for lis in lists:
    #     link='https://www.reifen.de/reifen/offroad_suv_4x4/andere?freeTextSearch=true&text={}&sort=popularity'.format(lis)
    #     start_urls.append(link)

    def parse(self, response):
        #products_results will collect the information of if GTIN product does not exist
        products_results=response.xpath('//*[@class="no-results-box__heading"]//text()').extract_first()
        link=response.xpath('//*[@class="search-result-view-offers"]//@href').extract_first()

        #request to parse_p
        yield scrapy.Request(
                                link,
                                meta={
                                'lis':response.xpath('//*[@id="js-search-filter-form"]').xpath('.//*[@name="freeText"]//@value').extract_first(),
                                'products_results':products_results,
                                }
                                ,callback=self.parse_p

                                )

    def parse_p(self, response):
        r_link=response.url # responding current url
        code=response.meta['lis'] #extracting meta data from parse method
        products_results=response.meta['products_results'] #extracting meta data from parse method

        tab_lists=response.css('section.tab-panel.active div.full-offer') # list of offer elements
        for tab in tab_lists:
            ShopName=tab.xpath('.//*[@class="offer-view-seller"]//@title').extract_first()
            Price=tab.css('div.offer-price span::text').extract() #Price for extracting with symbol like 100,00€
            Price=' '.join(Price)
            #you can use it for without symbol the price currency 
            # Price=tab.xpath('.//*[@itemprop="price"]//text()').extract_first() #If you need the data only. That's mean without symbol 100,00

            #finally we don't want to extract the value if the GTIN Product does not exist
            if products_results=="Für Ihre Auswahl sind derzeit keine Produkte mehr verfügbar.":
                ShopName=''
                Price=''
                code=''
            else:
                products_results='Query Found!'

            yield{
                'U-Link':r_link,
                'GTIN':code,
                'Products Results':products_results,
                'ShopName':ShopName,
                'Price':Price


            }

            # It's filtered to duplicate requests. The reason is if GTIN Product does not exist.
            # It's pull the request same url each time so it's and finally it's should be filtered





