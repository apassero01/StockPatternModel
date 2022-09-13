import pandas as pd
import yfinance as yf 
import pickle
import DataCollection.Stock as Stock
import os
from yahoo_fin import stock_info as si

class DataGrab:
    ticker  = ''
    lastDate = ''
    initialDataFrame = pd.DataFrame()

    def __init__(self, ticker): 
        self.ticker = ticker

    def initialDownload(self,startDate, endDate):
        initialDataFrame = yf.download(self.ticker, start = startDate, end = endDate)
        self.lastDate = endDate
        return initialDataFrame 

    def updateData(self, currentDate):
        newDataFrame = yf.download(self.ticker, start = self.lastDate, end = currentDate)
        self.lastDate = currentDate
        return newDataFrame 


class CreateDataSet: 


    def __init__(self):
        self.AllPriceData = { }
        self.startDate = '2001-01-01'
        
    
    def writeData(self):
        if len(self.AllPriceData.keys()) > 0: 
            with open('PatternAnalysis/SavedData/AllPriceData.pickle', 'wb') as f:
                pickle.dump(self.AllPriceData,f,protocol=pickle.HIGHEST_PROTOCOL)
    
    def readData(self):
        if os.path.isfile('PatternAnalysis/SavedData/AllPriceData.pickle'):
            with open('PatternAnalysis/SavedData/AllPriceData.pickle', 'rb') as f:
                try:
                    self.AllPriceData= pickle.load(f)
                except Exception:
                    pass

    
    def addTickers(self, tickers ):
        self.readData()
        for ticker in tickers:
            if ticker in self.AllPriceData.keys():
                continue 
            else:
                ##will need to add way to check for failed
                
                newStock = Stock.StockObject(ticker) 
                newStock.initializeData(self.startDate)
                self.AllPriceData[ticker] = newStock
        self.writeData()
    
    def updateTickers(self):
        self.readData()
        for stock in self.AllPriceData: 
            self.AllPriceData[stock].updateData()
        self.writeData() 

    
    def returnData(self): 
        self.readData()
        return self.AllPriceData

    def getTickers(self): 
        spticks = pd.DataFrame( si.tickers_sp500() )
        nasticks = pd.DataFrame( si.tickers_nasdaq() )
        dowticks = pd.DataFrame( si.tickers_dow() )

        spticks = spticks[0].values.tolist()
        nasticks = nasticks[0].values.tolist()
        dowticks = dowticks[0].values.tolist()

        allTickers = spticks + nasticks + dowticks
        return allTickers

    def clearBadTicks(self): 
        tickersToClear = []
        if len(self.AllPriceData) <= 0:
            self.AllPriceData = self.readData()
        for ticker in self.AllPriceData: 
            if len(self.AllPriceData[ticker].priceData) == 0: 
                tickersToClear += [ticker]

        for ticker in tickersToClear: 
            del self.AllPriceData[ticker]
        
        self.writeData()






    

     


        
