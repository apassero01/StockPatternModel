import DataCollection.Stock as stock
import pandas as pd 
import PriceAnalysis.Patterns.Patterns as patterns
import StatisticalAnalysis.DataOrganize.GapDataOrganize2 as organizer


'''
Class to backtest gap positions. Initial analysis of gap fills show most 
positions with tight stop losses. This backtester will be programmed to take a 
price target and stop loss of all collected gap positions. It will then simulate 
each position following the price period by period to exit and enter positions as 
close to the stopLoss as possible. (Market conditions do not allow for instantanious exit 
from a position in both cases of profit or loss this simulates real world trades on 
these positions at the time period)
'''
class GapBackTester: 

    initialBalance = 0
    balance = 0 
    positionSize = 100 
    positionResults = [] #List to represent percent gain/loss of all positions 

    def __init__(self,gapAbovePositions,priceTargetPercent,stopLossPercent,stockDictionary): 
        '''
        gapAbovePostions: all gapPositions generated from statistical analysis 
        priceTarget: - 
        stopLoss: - stopLossPercent (normalized relative to pattern size)
        stockDictionary - holds key value pair to stocks and Stock objects that 
        contain data such as period price data needed to simulate positions
        '''
        self.gapAbovePositions = gapAbovePositions 
        self.priceTargetpercent = priceTargetPercent
        self.stopLossPercent = stopLossPercent 
        self.stockDictionary = stockDictionary
    

    def testPositions(self): 
        '''
        Method to iterate position by positions and gathering and sending
        necessary data to the positionsSimulator 
        '''

        for i in range(len(self.gapAbovePositions)): 
            gapAbovePosition = self.gapAbovePositions[i]
            fillInstances = gapAbovePosition.fillInstances 
            ticker = gapAbovePosition.ticker
            stock = self.stockDictionary[ticker]

            for fill in fillInstances: 
                positionValue = self.positionSize 

                self.balance -= positionValue
                self.initialBalance -= positionValue

                positionValue = self.positionSimulator(stock,fill,self.positionSize)
                self.balance += positionValue

                percentGain = (positionValue - self.positionSize)/self.positionSize*100 

                self.positionResults.append(percentGain)




    


    def positionSimulator(self,stock,fill,positionEquity): 
        positionEquity = 100 

        entryDate = fill.entryDate
        entryPrice = fill.entryPrice.price 

        stopLossOffset = self.stopLossPercent * fill.totalFillPercent * entryPrice

        stopLoss = entryPrice - stopLossOffset 

        priceTargetOffset = self.priceTargetpercent * fill.totalFillPercent * fill.bottom.price

        priceTarget = fill.bottom.price + priceTargetOffset

        priceData = stock.priceData 

        shares = entryPrice/positionEquity

        isActive = True


        for index, period in priceData[entryDate:].iterrows(): 
            
            name = period.name
            if name == entryDate: 
                continue
            periodHigh = period["High"]
            periodLow = period["Low"]
            periodClose = period["Close"]
            periodOpen = period["Open"]

            if periodOpen < stopLoss: 
                loss = periodOpen * shares 
                positionEquity -= loss
                isActive = False
                break
            
            if periodLow < stopLoss: 
                loss = stopLoss * shares
                positionEquity -= loss
                isActive = False
                break 
            
            ##May come accross collision because on period time frame it is unknown which candle wick was formed first 
            #Should not cause major harm 

            if periodOpen > priceTarget: 
                profit = periodOpen * shares 
                positionEquity += profit
                isActive = False 
                break 
            
            if periodHigh > priceTarget: 
                profit = priceTarget * shares
                positionEquity += profit 
                isActive = False 
                break 

        return positionEquity






