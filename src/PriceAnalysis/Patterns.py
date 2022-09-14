class Price: 
    '''
    Price class holds relevant information to a certain price for a stock.
    '''
    EPSILON = .01

    
    def __init__(self,price,date): 
        '''
        @param price A numeric price value
        @param date The date at which the stock traded at this price
        '''
        self.price = price 
        self.date = date
    

    def addDate(self,date):
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
        

class Support: 
    
    def __init__(self,price, date):
        self.price = price 
        self.dates = [date]
        self.touches = 2
    
    def addTouch(self,date):
        self.dates+=[date]
        self.touches += 1
    
    def addDate(self,date):
        self.date += [date]


class Resistance: 
    
    def __init__(self,price, date):
        self.price = price 
        self.dates = [date]
        self.touches = 2
    
    def addTouch(self,date):
        self.dates+=[date]
        self.touches += 1
    
    def addDate(self,date):
        self.date += [date]




# def main(): 
#     price1 = Price(99)
#     price2 = Price(100)
#     price3 = Price(500); 
#     price4 = Price(501); 
#     price5 = Price(29.5)

#     lsit = [price1, price2, price3]
#     print(lsit.index(price5) )

# main()