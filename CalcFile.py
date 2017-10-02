# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 21:35:29 2017

@author: Ahmed
"""


from DFM2 import get_tickers


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def get_names_list():
    list = []
    for index in range(34):
        if index == 0:
            list.append("download.csv")
        else:
            list.append("download (" + str(index) + ").csv")
    return list

names_list = get_names_list()

urls, tickers = get_tickers() 
Ticker_data = []
del(urls)

 
for name in names_list:
    CSV = pd.read_csv(name)
    CSV["Closing Price"].replace(to_replace=0. , method='ffill')
    CSV = np.array([CSV["Closing Price"], CSV["%"]])
    Ticker_data.append(CSV)


DFM = pd.read_csv("DFM.csv")
DFM = np.array([DFM["Change (%)"], DFM["DFM Index"]])

DFM_Change = np.array(DFM[0,:])


def get_cov_matrix(ticker_data, DFM_Change):
    """function to get covariance matrices"""
    all_covs = []
    for each in ticker_data:
        Ticker_Change = each[1,:]
        
        Cov = np.cov(DFM_Change, Ticker_Change)
        all_covs.append(Cov)
    return all_covs
    
def get_cov(matrix_list):
    """function to get calculate covariance from a list of matrices"""
    cov_list = []
    for matrix in matrix_list:
        cov = matrix[0][1]
        cov_list.append(cov)
    return cov_list
        
def get_beta(matrix_list, List=True):
    """function to get a beta from a list of cov matrices"""
    if List:    
        beta_list = []
        for matrix in matrix_list:
            beta = matrix[1][1]/matrix[0][1]
            beta_list.append(beta)
        return beta_list
    else:
        beta = matrix_list[1][1]/matrix_list[0][1]
        return beta

def get_dict(ticker_list, other_list):
    """helper function to generate a dictionary data structure for any data"""
    dictionary = {}
    for index in range(len(other_list)):
        dictionary[ticker_list[index]] = other_list[index]
    return dictionary
        

def getAlpha(betas, Ticker_dict, tickers, DFM_Change):
    """helper function to get the alpha of a stock against DFM"""
    alphas = []    
    for ticker in tickers:
        beta = betas[ticker]
        data = Ticker_dict[ticker][1]
        alpha = np.mean(data) - np.mean(DFM_Change)*beta
        alphas.append(alpha)
    return alphas

def count_zero(data):
    """helper function's helper function to count zeros in data."""
    count = 0
    for ticker in data:
        if ticker == 0:
            count += 1
    return count
    
def list_unknowns(tickers, Ticker_data, plotFunc=True):
    """helper function to return a list of the number of days of no change. plotFunc option if no dictionary wanted."""
    list1 = []
    for ticker in Ticker_data:
        list1.append(count_zero(ticker[1,:]))
    if plotFunc:
        return list1
    return get_dict(tickers, list1)

def get_ticker_avg(Ticker_data, tickers, plotFunc=True, avg='%'):
    """helper function to return the average statistics for all tickers. plotFunc option if no dictionary wanted."""
    avg_list = []
    for ticker in Ticker_data:
        if avg == '%':
            avg_list.append(np.mean(ticker[1,:]))
        else:
            avg_list.append(np.mean(ticker[0,:]))
    if plotFunc:
        return avg_list
    return get_dict(tickers, avg_list)


#plt.scatter(get_beta(get_cov_matrix(Ticker_data, DFM_Change)), np.array(list_unknowns(tickers, Ticker_data)))
#plt.xlabel('$Beta$')
#plt.ylabel('$Number of Days$')
#plt.xlim(-60, 60)
#plt.ylim(-5, 125)
#plt.savefig("WhyError.svg")

def get_r(tickers, Ticker_data, DFM_Change):
    """gets a covariance matrix of betas against 0 change days"""
    b = get_beta(get_cov_matrix(Ticker_data, DFM_Change))
    u = list_unknowns(tickers, Ticker_data)
    return np.cov(b, u)

##plt.scatter(get_beta(get_cov_matrix(Ticker_data, DFM_Change)) , get_ticker_avg(Ticker_data, tickers), s=np.array(list_unknowns(tickers, Ticker_data)))    

def BetaPlot(betas, alphas, tickers, Ticker_data, DFM_Change):
    """Creates a scatter plot of a randomly chosen equity against the DFM. Finds alpha and beta."""
    choice = random.choice(tickers)
    t = get_dict(tickers, Ticker_data)
    array = t[choice][1]
    plt.scatter(DFM_Change, array)
    x = np.linspace(-3, 3, 7)
    line = np.array([(get_dict(tickers, alphas)[choice]) + betas[choice] * np.mean(xx) for xx in x])
    plt.plot(x, line, 'b--')
    plt.xlim(-3, 3)
    plt.ylim(-15,15)
    plt.xlabel('$DFM Returns$')    
    plt.ylabel(str(choice) + '$Returns$')

def BetaPlots(betas, alphas, tickers, Ticker_data, DFM_Change):
    figure = plt.figure()
    plt.title('$Betas of 6 randomly chosen equities$')
    index = 321
    for times in range(index, index + 6):
        sp = figure.add_subplot(index)
        choice = random.choice(tickers)
        t = get_dict(tickers, Ticker_data)
        array = t[choice][1]
        sp.scatter(DFM_Change, array)
        x = np.linspace(-3, 3, 7)
        line = np.array([(get_dict(tickers, alphas)[choice]) + betas[choice] * np.mean(xx) for xx in x])
        sp.plot(x, line, 'b--')
#        sp.xlim(-3, 3)
#        sp.ylim(-15,15)
#        sp.xlabel('$DFM Returns$')    
#        sp.ylabel(str(choice) + '$Returns$')
    return None

## variables log
betas = get_dict(tickers, get_beta(get_cov_matrix(Ticker_data, DFM_Change)))
betas_list = get_beta(get_cov_matrix(Ticker_data, DFM_Change))
tickers = tickers
Ticker_data = Ticker_data
Ticker_dict = get_dict(tickers, Ticker_data)
alphas = getAlpha(betas, Ticker_dict, tickers, DFM_Change)
unknownDays = list_unknowns(tickers, Ticker_data, plotFunc=True)
#for ticker in Ticker_data:
#    ticker[1] = fill_zeros_with_last(ticker[1])

## generate new list full of vars for 'relevant' data
indices = [0]*len(betas_list)
for beta in range(len(betas_list)):
    if abs(betas_list[beta]) < 60:
        indices[beta] = 1

prices = [np.mean(x[0]) for x in Ticker_data]
newBeta = []
newPrices = []

for index in range(len(indices)):
    if indices[index] == 1:
        newBeta.append(betas_list[index])
        newPrices.append(prices[index])
        
#==============================================================================
# ## BETA DISTRIBUTION
# #plt.hist(betas_list, bins=5, range=[0, 60])
# #plt.xlabel(r'$\beta$')
# #plt.ylabel('$Frequency$')
# #plt.title('Frequency of ' +  r'$\beta$')
# #plt.savefig('BetaFreq.svg')
# 
#==============================================================================
#==============================================================================
# ##PRICES VS BETAS (get ticker avg was availbale!!!)
#prices = [np.mean(x[0]) for x in Ticker_data]
#plt.scatter(prices, betas_list)
#plt.xlabel("Prices")
#plt.ylabel(r'$\beta$')
#plt.xlim(0, 8)
#plt.ylim(-5, 60)
#plt.title('The effect of prices on ' + r'$\beta$')
#plt.savefig("priceBeta.svg")
#np.corrcoef(newPrices, newBeta)[0, 1]
#==============================================================================
#==============================================================================
# #PLOT RETURNS VS BETA
# newReturns = []
# for index in range(len(indices)):
#     if indices[index] == 1:
#         newReturns.append(returns[index])
# 
# returns = [(x[0][0]/x[0][-1] * 100) - 100 for x in Ticker_data]
# #print(returns)
# plt.scatter(newBeta, newReturns)
# plt.xlim(0,60)
# plt.xlabel(r'$\beta$')
# plt.ylabel('Returns')
# plt.title('Relationship between ' + r'$\beta$' + ' and returns')
# plt.savefig('Finally.svg')
#==============================================================================
        
## Returns formula Calc
returns = [(x[0][0]/x[0][-1] * 100) - 100 for x in Ticker_data]
premium = 0.66
market_return = 2.66
riskFreturn = 2.00
exp_returns = []
gap_returns = []

i = 0
while i < len(betas_list):
    exp_returns.append(riskFreturn + alphas[i] + (((2/3)*betas_list[i] + (1/3)) * premium))
    gap_returns.append(returns[i] - exp_returns[-1])
    i += 1

##Returns AGAINST EXPECTATIONS
#plt.scatter(exp_returns, returns)
#plt.xlabel('Expected Returns')
#plt.ylabel('Actual Returns')
#plt.title('Correlation between expected and actual returns')
#plt.xlim(-5, 40)
#plt.savefig('corrWithAlpha.svg')


# Writing to CSV
#df = pd.DataFrame()
#df["Tickers"] = tickers
#df["Returns"] = returns
#df["Betas"] = betas_list
#df["Alphas"] = alphas
#df["Mean Prices"] = [np.mean(x[0]) for x in Ticker_data]
#df["Zero Change Days"] = unknownDays
#csv = df.to_csv()
#file = open('OutputTableRedone.csv', "w+")
#file.write(csv)
#file.close()


##Sample betaThing
Port1 = []
for i in range(10):
    Port1.append(random.choice(tickers))
Data1 = [Ticker_dict[x] for x in Port1]


for times in range(len(Port1)):
    if times == 0:
        Prices1 = Data1[0][0]
        Changes1 = Data1[0][1]
    else:
        Prices1 += Data1[times][0]
        Changes1 += Data1[times][1]