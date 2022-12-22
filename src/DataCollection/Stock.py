import DataCollection.ImportData as importdata
import PriceAnalysis.Patterns as patterns
from datetime import date
import pandas as pd
import yfinance as yf
import pickle

'''
Class encapsulates a stock object. Each stock object will contain its 
own price data, with varius technical statistics 
'''
class StockObject: 
    ticker = ""
    relativeMin = []
    relativeMax = []
    support = []
    levels = []



    '''
    Initialize a stock object with a ticker. An instance 
    of the class "DataGrab" is also created to be used for 
    downloading price data. 
    '''
    def __init__(self, ticker):
        self.ticker = ticker
        self.dataGrab = importdata.DataGrab(ticker)
        
    
    '''
    Download all up to current date and store in self.priceData
    '''
    def initializeData(self, startDate): 
        self.updateCurrentDate()
        self.priceData = self.dataGrab.initialDownload( startDate, self.currentDate )

    '''
    For stock that already contains priceData, update that data to currentDate 
    '''
    def updateData(self):
        self.updateCurrentDate()
        updatedPriceDate = self.dataGrab.updateData(self.currentDate)
        frames = [self.priceData, updatedPriceDate]
        self.priceData = pd.concat(frames)

    
    '''
    Update the current date 
    '''
    def updateCurrentDate(self):
        self.currentDate = date.today()
        self.currentDate = self.currentDate.strftime("%Y-%m-%d")

    '''
    output the priceData to the console 
    '''
    def printData(self):
        print(self.priceData)
    
    def getLevels(self):
        return self.levels