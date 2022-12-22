import PriceAnalysis.Patterns as Patterns
from PriceAnalysis.Patterns import Price
import PriceAnalysis.PatternContainers as containers
import pandas as pd 


class FindPatterns:
    '''
    Class FindPatters iterates over every date creating instances of support 
    and levels and checks for predefined patterns. 
    '''

    #SwingChange is the percent range away from the current price that a previous high or low is considered a relitive high or low
    SWINGCHANGE = .07
    GAPSIZEPERCENT = .07 




    def __init__(self,stock):
        '''
        Initializes FindPatterns object 
        @param Stock object of type Stock
        '''
        self.curStock = stock
        self.ticker = self.curStock.ticker
        self.priceData = self.curStock.priceData
        self.currentLevels = []
        self.support = self.curStock.support
        self.relativeHighs = []
        self.relativeLows = []
        self.gapContainer = containers.GapContainer()  


    

    def analyzePriceData(self):
        '''
        Method to loop over a stocks panda dataset containing relavent price data checking for patterns. 
        '''


        relMax = Patterns.Price(0)
        relmin = Patterns.Price(0)

        prevPeriod = pd.DataFrame() 

        for index, period in self.priceData.iterrows(): 
            
            periodHigh = period["High"]
            periodLow = period["Low"]
            periodOpen = period["Open"]
            periodClose = period["Close"]
            date = period.name
            
        

            periodHigh = Patterns.Price(periodHigh,date)
            periodLow = Patterns.Price(periodLow,date)
            periodOpen = Patterns.Price(periodClose,date)

            if not prevPeriod.empty:
                self.checkForGap(periodOpen,Patterns.Price(prevPeriod["Close"],prevPeriod.name))
            self.gapContainer.analyzeGaps(periodHigh) 


            # self.currentLevels += [Patterns.PriceLevels("resistance",periodHigh,date)]
            closestlevels = self.getClosestlevels(periodHigh)

            if periodHigh > relMax: 
                relMax = periodHigh
                relMax.setDate(date)
            
            #Considered far enough away from previus high to consider price a relative high 
            if periodLow.price < relMax.price-relMax.price*self.SWINGCHANGE: 
                self.addRelativeHigh(relMax,date)
                relMax = periodHigh
            if periodHigh == closestlevels.price:
                ##TODO check for both support and resistance 
                closestlevels.addResisTouch(date)
            

            #End of each day store date to be accessed at the next date
            prevPeriod = period 
            

        

           
    def checkForGap(self,periodOpen,prevClose):
        percentChange = ((periodOpen - prevClose)/prevClose).price
        if abs(percentChange) < self.GAPSIZEPERCENT:
            return
        self.gapContainer.addGap(periodOpen,prevClose,percentChange)

        



    def addRelativeHigh(self,relMax,date):
        '''
        Method to add relative high to list of other relative highs. 
        If it already exists in the list relative high is removed and a levels
        object is istantiated at that price. 
        '''
        
        if (relMax in self.relativeHighs):

            repeatMax = self.relativeHighs[self.relativeHighs.index(relMax)]
            newLevel = Patterns.PriceLevels("resistance", relMax,relMax.date)
            newLevel.addDate("resistance",repeatMax.date)
            self.relativeHighs.remove(relMax)
            if (newLevel not in self.currentLevels): 
                self.currentLevels += [newLevel]
        else: 
            self.relativeHighs += [relMax]
    

    def getClosestlevels(self,price):
        ##TODO return support and resistance values
        difference = price; 
        closestIndex = 0; 

        if len(self.currentLevels) == 0:
            
            return Patterns.PriceLevels("support", Patterns.Price(0),'01-01-2001')
        
        for index,curlevels in enumerate(self.currentLevels): 
            if abs(price-curlevels.price) < difference: 
                difference = abs(price-curlevels.price)
                closestIndex = index 
        
        return self.currentLevels[closestIndex]
        
    
    def returnStock(self):
        self.curStock.levels = self.currentLevels
        return self.curStock
        

        
        
