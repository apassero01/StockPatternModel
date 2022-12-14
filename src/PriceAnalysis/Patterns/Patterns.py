class Price: 
    '''
    Price class holds relevant information to a certain price for a stock.
    '''
    EPSILON = .01

    
    def __init__(self,price,date = None): 
        '''
        @param price A numeric price value
        '''
        self.price = price 
        self.date = date
    

    def setDate(self,date):
        '''
        Add date value to list for multiple occurances of self price
        '''
        self.date = date
    
    def __eq__(self,otherPrice):
        '''
        Overrides equality to allow prices to be considered equal if they are within percent range EPSILON
        '''
        rangeOfEquality = self.price* self.EPSILON
        if otherPrice.price >= self.price - rangeOfEquality and otherPrice.price <= self.price+rangeOfEquality:
            return True
        else:
            return False
    
    def __sub__(self,other):
        return Price(self.price - other.price)
    
    def __add__(self,other):
        return Price(self.price + other.price)

    def __truediv__ (self,other):
        return Price(self.price/other.price)


    def __gt__(self,other):
        return (self.price > other.price)
    
    def __lt__(self,other):
        return (self.price < other.price)

    def __repr__(self):
        return str(round(self.price,4))
    
    def __abs__(self):
        if self.price > 0: 
            return Price(self.price)
        else:
            return Price(self.price*-1)
        
class Candle: 
    def __init__(self,open,close,high,low,date):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.date = date


class PriceLevels: 
    
    def __init__(self,levelType, price, date):
        self.price = price 
        if levelType == "support":
            self.supportDates = [date]
            self.resistanceDates = []
            self.supportTouches = 2; 
            self.resistanceTouches = 0; 
        else: 
            self.support = []
            self.resistanceDates = [date]
            self.supportTouches = 0
            self.resistanceTouches = 2 
    
    def addResisTouch(self,date):
        self.resistanceDates+=[date]
        self.resistanceTouches += 1
    
    def addSupportTouch(self,date):
        self.supportDates+=[date]
        self.supportTouches += 1
    
    def addDate(self,levelType, date,):
        if levelType == "support":
            self.supportDates += [date]
        else:
            self.resistanceDates += [date]

    
    def __eq__(self,other):
        return self.price == other.price

    def __repr__(self):
        ##TODO update repr for support and resistance 
        resisString = str(self.price) + " "
        resisString += str(self.resistanceTouches)
        # for date in self.dates:
        #     resisString += date.strftime("%Y-%m-%d") + " "
        return resisString
    
    def getTotalTouches(self):
        return self.resistanceTouches + self.supportTouches
