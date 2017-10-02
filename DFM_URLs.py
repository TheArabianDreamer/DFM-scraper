"""
program to collect all of the DFM ticker symbols
scraped from http://www.dfm.ae/sharia/companies-classification/classification-list-page?q=1&y=2017&e=dfm
BeautifulSoup4

Module returns a list of URLS for each ticker in the DFM
"""
import bs4 as bs
import requests
import string


def get_url_tickers():
    print("Loading URL Tickers:\nPlease allow 10 seconds for data to load")
    sauceDFM = requests.get('http://www.dfm.ae/sharia/companies-classification/classification-list-page?q=1&y=2017&e=dfm')
    soupDFM = bs.BeautifulSoup(sauceDFM.text, 'lxml')
    table = soupDFM.findAll(name='td')
    table = table[4:] ##some of that earlier stuff is unnecessary


    tickers = [] #output variable
    for i in range(len(table)):
        if (i - 1) % 4 == 0:
            tickers.append(table[i])

    ##remove <td> tags
    newTickers = [] ##corrected output variable
    for ticker in tickers:
        ticker = str(ticker)
        new_ticker = ''
        for char in ticker:
            if char in string.ascii_uppercase: ##remove all the lowercase etc. which obviously is not part of the ticker
                new_ticker += char
        newTickers.append(new_ticker)
                
    base_url = "http://www.dfm.ae/en/issuers/listed-securities/securities/company-profile-page?id="
    urlList = []
    for ticker in newTickers:
        urlList.append(base_url + ticker)
        
    print()
    print("Done: There are " + str(len(newTickers)) + " tickers loaded")
    return urlList, newTickers


"""
Obtained a list of URLs which seem to work quite well. Note that the list appears not to be complete. There are 67 companies listed on the index, of which only 38 are loaded up. 29 missing. 19 possibly NASDAQ Dubai?
"""