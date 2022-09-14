import Patterns


class FindPatterns:
    '''
    Class FindPatters iterates over every date creating instances of support 
    and resistance and checks for predefined patterns. 
    '''

    #SwingChange is the percent range away from the current price that a previous high or low is considered a relitive high or low
    SWINGCHANGE = .05
    relativeHighs = []
    relativeLows = []


    def __init__(self,stock):
        '''
        Initializes FindPatterns object 
        @param Stock object of type Stock
        '''
        self.stock = stock
        self.ticker = stock.ticker
        self.priceData = stock.priceData
        self.resistance = stock.resistance
        self.support = stock.support
        
    

    def analyzePriceData(self):
        '''
        Method to loop over a stocks panda dataset containing relavent price data checking for patterns. 
        '''

        relMax = 0
        relmin = 0

        for index, period in self.priceData.iterrows(): 
            periodHigh = period["High"]
            periodLow = period["Low"]
            date = period["Date"]

            if periodHigh > relMax: 
                relMax = periodHigh 
            
            #Considered far enough away from previus high to consider price a relative high 
            if periodHigh < relMax+relMax*self.SWINGCHANGE: 
                self.addRelativeHigh(relMax,date)


    def addRelativeHigh(self,relMax,date):
        '''
        Method to add relative high to list of other relative highs. 
        If it already exists in the list relative high is removed and a resistance
        object is istantiated at that price. 
        '''
        relMax = Patterns.Price(relMax,date)
        
        if (relMax in self.relativeHighs):
            repeatMax = self.relativeHighs[self.relativeHighs.index(relMax)]
            newResistance = Patterns.Resistance(relMax,date)
            newResistance.addDate(repeatMax.date)
            self.relativeHighs.remove(relMax)
            self.resistance += [newResistance]
        else: 
            self.relativeHighs += [relMax]

        
        
