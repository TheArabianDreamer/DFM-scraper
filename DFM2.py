# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 22:06:51 2017

@author: Ahmed
"""

import bs4 as bs
from selenium import webdriver
import string
import time


###Configure website
#DFM = webdriver.Chrome()
#DFM.get('http://marketwatch.dfm.ae/?isRedirected=true')
#
###Click the 'Traded Equities' button. Also get only DFM equities
#time.sleep(10)
#tradedOnly = DFM.find_element_by_class_name("showtradedlabel")
#tradedOnly.click()
#exchangeMenu = DFM.find_element_by_xpath('//*[@id="exchange-filter"]/div/button')
#exchangeMenu.click()
#DFMExchange = DFM.find_element_by_xpath('//*[@id="exchange-filter"]/div/ul/li[1]/a/label')
#DFMExchange.click()


"""Note that the webscraping algorithm shown below seems not to work. We have obtained the tickers manually"""
##Get the source of the desirable page
#html = DFM.page_source
#soup = bs.BeautifulSoup(html, 'lxml')

##Get table data

#table = soup.find_all(name="span" , attrs={"class": "name-symbol"})
#print(table)

def get_tickers():
    #file = input("Please enter the filename: (It should be tradedTickers.txt)")
    file = "tradedTickers.txt"
    text = open(file, "r")
    tickers = text.read().split(',')
    
    base_url = "http://www.dfm.ae/en/issuers/listed-securities/securities/company-profile-page?id="
    urlList = []
    for ticker in tickers:
        urlList.append(base_url + ticker)
        
    print()
    print("Done: There are " + str(len(tickers)) + " tickers loaded")
    return urlList, tickers
    
x, y = get_tickers()