# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 22:29:13 2017

test script: selenium downloads

@author: Ahmed
"""

from selenium import webdriver
import DFM2
import time

def get_CSV(urls):
    browser = webdriver.Chrome()
    
    for url in urls:
    
        browser.get(url)
        
        time.sleep(10)
        SixMonths = browser.find_element_by_xpath('//*[@id="tab-1"]/div[1]/div[2]/div[1]/label[5]')
        SixMonths.click()
        
        DailySum = browser.find_element_by_xpath('//*[@id="companyProfileTabsInner"]/li[2]/a')
        DailySum.click()
        
        Download = browser.find_element_by_xpath('//*[@id="secondTable"]')
        Download.click()
        
    browser.close()

urls, tickers = DFM2.get_tickers()

get_CSV(urls)
    
    
"""
This code works. It automatically downloads the relevant files into the downloads folder. To be manually exported later
"""


