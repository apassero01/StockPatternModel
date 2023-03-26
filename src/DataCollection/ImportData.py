import pandas as pd
import yfinance as yf 
import pickle
import DataCollection.Stock as Stock
import os
from yahoo_fin import stock_info as si

class DataGrab:
    '''
    Class to download and update data for a stocks string "ticker"
    '''
    ticker  = ''
    lastDate = ''
    initialDataFrame = pd.DataFrame()

    def __init__(self, ticker): 
        '''
        @param ticker String of stocks "ticker" 
        '''
        self.ticker = ticker

    def initialDownload(self,startDate, endDate):
        '''
        Downloads initial dataset from yahoo finance libray 
        @param startDate and endDate in the form 'YYYY-MM-DD'
        @return pandas dataframe with price data
        '''
        initialDataFrame = yf.download(self.ticker, start = startDate, end = endDate)
        self.lastDate = endDate
        return initialDataFrame 

    def updateData(self, currentDate):
        '''
        Updates data of ticker to current date. 
        @param current date in the form 'YYYY-MM-DD'
        @return updated panda dataframe 
        '''
        newDataFrame = yf.download(self.ticker, start = self.lastDate, end = currentDate)
        self.lastDate = currentDate
        return newDataFrame 


class CreateDataSet:
    '''
    Class to create dataset of stocks 
    ''' 


    def __init__(self):
        self.AllPriceData = { }
        self.startDate = '2016-01-01'
        
    
    def writeData(self,stockDict):
        '''
        Writes data from AllPriceData dictionary to a pickle file.
        '''
        if len(stockDict.keys()) > 0: 
            with open('SavedData/AllPriceData.pickle', 'wb') as f:
                pickle.dump(stockDict,f,protocol=pickle.HIGHEST_PROTOCOL)
    
    def readData(self):
        '''
        Reads data from a pickle file to AllPriceData dictionary.
        '''
        if os.path.isfile('SavedData/AllPriceData.pickle'):
            with open('SavedData/AllPriceData.pickle', 'rb') as f:
                try:
                    self.AllPriceData= pickle.load(f)
                except Exception:
                    pass

    

    def addTickers(self, tickers):
        '''
        Add stock data for a list of tickers to already created dataSet
        @param tickers a list of stock tickers
        '''

        self.readData()
        for ticker in tickers:
            if ticker in self.AllPriceData.keys():
                continue 
            else:
                ##TODO need to add way to check for failed
                
                newStock = Stock.StockObject(ticker) 
                newStock.initializeData(self.startDate)
                self.AllPriceData[ticker] = newStock
        self.writeData(self.AllPriceData)
    
    def updateTickers(self):
        '''
        Updates all the tickers to current data in the pickle file. 
        '''
        self.readData()
        for stock in self.AllPriceData: 
            self.AllPriceData[stock].updateData()
        self.writeData() 

    
    def returnData(self): 
        '''
        @return dictionary of the price data for all stocks in data file. Key: "ticker" value: Stock object
        '''
        self.readData()
        return self.AllPriceData


    def generateTickers(self): 
        '''
        Generates a list of tickers from the S&P500, NASDAQ and DOW
        '''
        spticks = pd.DataFrame( si.tickers_sp500() )
        # nasticks = pd.DataFrame( si.tickers_nasdaq() )
        dowticks = pd.DataFrame( si.tickers_dow() )

        spticks = spticks[0].values.tolist()
        # nasticks = nasticks[0].values.tolist()
        dowticks = dowticks[0].values.tolist()

        allTickers = spticks + dowticks
        return allTickers

    def clearBadTicks(self): 
        '''
        Removes tickers from dataset that failed to download
        '''
        tickersToClear = []
        if len(self.AllPriceData) <= 0:
            self.AllPriceData = self.readData()
        for ticker in self.AllPriceData: 
            currentStock = self.AllPriceData.get(ticker)
            if len(currentStock.priceData) == 0: 
                tickersToClear += [ticker]

        for ticker in tickersToClear: 
            del self.AllPriceData[ticker]
        
        
        
        self.writeData(self.AllPriceData)






    

     


        
