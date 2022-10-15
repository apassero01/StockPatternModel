import DataCollection.ImportData as importdata
import PriceAnalysis.Patterns as patterns
from datetime import date
import pandas as pd
import yfinance as yf
import pickle

class StockObject: 
    ticker = ""
    relativeMin = []
    relativeMax = []
    support = []
    levels = []



    def __init__(self, ticker):
        self.ticker = ticker
        self.dataGrab = importdata.DataGrab(ticker)
    
    def initializeData(self, startDate): 
        self.updateCurrentDate()
        self.priceData = self.dataGrab.initialDownload( startDate, self.currentDate )

    def updateData(self):
        self.updateCurrentDate()
        updatedPriceDate = self.dataGrab.updateData(self.currentDate)
        frames = [self.priceData, updatedPriceDate]
        self.priceData = pd.concat(frames)

    
    def updateCurrentDate(self):
        self.currentDate = date.today()
        self.currentDate = self.currentDate.strftime("%Y-%m-%d")

    def printData(self):
        print(self.priceData)

    def addSuport(self,price,date):
        if price in self.support.keys():
            self.support[price].addTouch() 
        else: 
            self.support[price] = patterns.Support(price,date)
             



    # def analyze(self):
    #     upTrend = True
    #     for index, row in self.priceData.iterrows: 
    #         print("hello")

    # def getMovingAverage(self, period): 
    #     self.movingAverage50 += period; 

# def main():
#     ticker = "aapl"
#     startDate = '2001-01-01'
#     endDate = '2021-01-01' 
#     apple = Stock(ticker)
#     apple.initializeData(startDate)
#     apple.updateData()
#     ticker2 = "tsla"
#     tsla = Stock(ticker2)
#     tsla.initializeData(startDate)
#     tsla.updateData()
#     with open('data2.pickle', 'wb') as f:
#         pickle.dump([apple, tsla],f) 


# main()