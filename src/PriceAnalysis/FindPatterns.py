import PriceAnalysis.Patterns as Patterns
from PriceAnalysis.Patterns import Price


class FindPatterns:
    '''
    Class FindPatters iterates over every date creating instances of support 
    and levels and checks for predefined patterns. 
    '''

    #SwingChange is the percent range away from the current price that a previous high or low is considered a relitive high or low
    SWINGCHANGE = .07
    relativeHighs = []
    relativeLows = []
    levels = []


    def __init__(self,stock):
        '''
        Initializes FindPatterns object 
        @param Stock object of type Stock
        '''
        self.stock = stock
        self.ticker = stock.ticker
        self.priceData = stock.priceData
        self.levels = stock.levels
        self.support = stock.support
        
    

    def analyzePriceData(self):
        '''
        Method to loop over a stocks panda dataset containing relavent price data checking for patterns. 
        '''

        relMax = Patterns.Price(0)
        relmin = Patterns.Price(0)

        for index, period in self.priceData.iterrows(): 
            periodHigh = period["High"]
            periodLow = period["Low"]
            date = period.name

            periodHigh = Patterns.Price(periodHigh,date)
            periodLow = Patterns.Price(periodLow,date)
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
            if (newLevel not in self.levels): 
                self.levels += [newLevel]
        else: 
            self.relativeHighs += [relMax]
    

    def getClosestlevels(self,price):
        ##TODO return support and resistance values
        difference = price; 
        closestIndex = 0; 

        if len(self.levels) == 0:
            
            return Patterns.PriceLevels("support", Patterns.Price(0),'01-01-2001')
        
        for index,curlevels in enumerate(self.levels): 
            if abs(price-curlevels.price) < difference: 
                difference = abs(price-curlevels.price)
                closestIndex = index 
        
        return self.levels[closestIndex]
        
        

        
        
