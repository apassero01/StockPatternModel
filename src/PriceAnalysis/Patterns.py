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


class GapAbove:
    
    '''
    Initializes top and bottom of gap along with whether the current price level
    has entered the gap and if it has been filled. 
    highestPercentFilled - List of values for highest percent filled for every instance that price entered and left the gap. 
    '''
    def __init__(self,top,bottom):
        self.top = top
        self.bottom = bottom
        self.inside = False
        self.filled = False
        self.percentFilled = 0 
        self.highestPercentFilled = [] 
        self.totalFillPercent = ((self.top-self.bottom)/self.bottom).price

    def updateGap(self,price): 
        if price > self.bottom:
            self.inside = True
            tempFill = (((price-self.bottom)/self.bottom)).price
            self.percentFilled = max(tempFill,self.percentFilled)
            self.percentFilled = min(self.percentFilled,1)

            if self.percentFilled > 1: 
                self.filled = True
        else: 
            if self.inside: 
                self.highestPercentFilled.append(round(self.percentFilled/self.totalFillPercent*100,4));    
            self.inside = False
            self.percentFilled = 0
            
            

    def __eq__(self,other):
        if isinstance(other,GapAbove):
            return self.bottom == other.bottom
        return False
    def __gt__(self,other):
        return self.bottom > other.bottom
    def __lt__(self,other):
        return self.bottom < other.bottom
    def __repr__(self):
        s = "\nGap Above \n"
        s+="Date: " + self.top.date.strftime("%m/%d/%Y") + "\n"
        s+= "Size: " + str(self.totalFillPercent*100)+"%\n"
        s+="List of Percent Fill Instances: "+ str(self.highestPercentFilled)+"\n"
        s+="Bottom = " + str(self.bottom) + " Top = " + str(self.top) + "\n"
        return s

'''
    Initializes top and bottom of gap along with whether the current price level
    has entered the gap and if it has been filled. 
    highestPercentFilled - List of values for highest percent filled for every instance that price entered and left the gap. 
    '''
class GapBelow:
    def __init__(self,top,bottom):
        self.top = top
        self.bottom = bottom
        self.inside = False 
        self.filled = False
        self.percentFilled = 0 
        self.highestPercentFilled = []
        self.totalFillPercent = ((self.top-self.bottom)/self.top).price

    def updateGap(self,price): 
        if price < self.top:
            self.inside = True
            tempFill = (((self.top-price)/self.top)).price/self.totalFillPercent
            self.percentFilled = max(tempFill,self.percentFilled)
            self.percentFilled = min(self.percentFilled,1)

            if self.percentFilled > 1: 
                self.filled = True
        else: 
            if self.inside: 
                self.highestPercentFilled.append(round(self.percentFilled/self.totalFillPercent*100,4));    
            self.inside = False
            self.percentFilled = 0; 
            
    
    def __eq__(self,other): 
        if isinstance(other,GapBelow):
            return self.top == other.top
        return False
    def __gt__(self,other):
        return self.top > other.top
    def __lt__(self,other):
        return self.top < other.top

    def __repr__(self):
        s = "\nGap Below \n"
        s+="Date: " + self.bottom.date.strftime("%m/%d/%Y") + "\n"
        s+= "Size: " + str(self.totalFillPercent*100)+"%\n"
        s+="List of Percent Fill Instances: "+ str(self.highestPercentFilled)+"\n"
        s+="Bottom = " + str(self.bottom) + " Top = " + str(self.top) + "\n"
        return s