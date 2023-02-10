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
        self.fillInstances = []
        self.currentFill = None
        self.totalFillPercent = ((self.top-self.bottom)/self.bottom).price
        self.newFill = False 
        self.below = False
        self.sameDayFill = False

    '''
    Method for updating the currentGap to the most recent price. 
    @candle is a candle object containing the period high,low,open,close,date
    Method checks if there is a current gapAboveFill instance and updates it accordingly. 
    A gapAboveFill instance is considered active if price is within the gap or has been outside of the gap
    for a maximum of one day. 
    '''
    def updateGap(self,candle): 
        if candle.close > self.bottom:
            self.inside = True
            if self.currentFill == None: 
                self.currentFill = GapAboveFill(candle.close,self.totalFillPercent,self.top,self.bottom)
                self.newFill = True
                self.sameDayFill = False
            else:
                self.newFill = False 
            
            self.currentFill.updateFill(candle) 

            if self.currentFill.percentFilled > self.totalFillPercent*.75: 
                self.filled = True
                self.fillInstances.append(self.currentFill)
                if self.currentFill.daysInside == 1: 
                    self.sameDayFill = True
                self.currentFill = None
                
            
        else: 
            self.newFill = False 
            if self.inside: 
                self.currentFill.updateFill(candle)
                if not self.currentFill.active:
                    ##When a GapFill instance is no longer active, it is added to the list of fill instances 
                    self.fillInstances.append(self.currentFill)
                    self.inside = False
                    self.currentFill = None  
            
    def setNewMin(self,minPrice):
        if self.sameDayFill and len(self.fillInstances) > 1: 
            lastFill = self.fillInstances[-2]
        else:
            lastFill = self.fillInstances[-1]
            
        if lastFill.percentFilled  > self.totalFillPercent:
            return 

        lastFill.minAfterExit = min(lastFill.minAfterExit,minPrice) 

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
        s+= "Size: " + str(round(self.totalFillPercent*100,2))+"%\n"
        s+="List of Percent Fill Instances: "+ str(self.fillInstances)+"\n"
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
        self.fillInstances = [] 
        self.currentFill = None
        self.totalFillPercent = ((self.top-self.bottom)/self.top).price
        self.newFill = False 
        self.below = True
        self.sameDayFill = False

    '''
    Method for updating the currentGap to the most recent price. 
    @candle is a candle object containing the period high,low,open,close,date
    Method checks if there is a current gapBelowFill instance and updates it accordingly. 
    A gapBelowFill instance is considered active if price is within the gap or has been outside of the gap
    for a maximum of one day. 
    '''
    def updateGap(self,candle): 
        if candle.close < self.top:
            self.inside = True
            if self.currentFill == None: 
                self.currentFill = GapBelowFill(candle.close,self.totalFillPercent,self.top,self.bottom)
                self.newFill = True
                self.sameDayFill = False
            else: 
                self.newFill = False 
            
            self.currentFill.updateFill(candle) 

            if self.currentFill.percentFilled > self.totalFillPercent*.75: 
                self.filled = True
                self.fillInstances.append(self.currentFill)
                if self.currentFill.daysInside == 1: 
                    self.sameDayFill = True
                self.currentFill = None
                
        else: 
            self.newFill = False
            if self.inside: 
                self.currentFill.updateFill(candle)
                if not self.currentFill.active: 
                    self.fillInstances.append(self.currentFill)
                    self.inside = False
                    self.currentFill = None  
    
    def setNewMax(self,maxPrice):
        
        if self.sameDayFill and len(self.fillInstances) > 1: 
            lastFill = self.fillInstances[-2]
        else:
            lastFill = self.fillInstances[-1]
        
        if lastFill.percentFilled  > self.totalFillPercent:
            return 
        lastFill.maxAfterExit = max(lastFill.maxAfterExit,maxPrice) 

    


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
        s+= "Size: " + str(round(self.totalFillPercent*100,2))+"%\n"
        s+="List of Percent Fill Instances: "+ str(self.fillInstances)+"\n"
        s+="Bottom = " + str(self.bottom) + " Top = " + str(self.top) + "\n"
        return s




class GapAboveFill: 
    """
    Class to encapsulate the data points that represent a gap fill. Price may enter and attempt 
    to fill a gap multiple times. A GapAboveFill object is one of these attempts. It remains active 
    while price closes within the gap or closes outside for a maximum of one day 

    Attribues: 
    top : Price - top of gap
    bottom: Price - buttom of gap
    percentFilled: float - percent gain within gap / total percent size of gap 
    percentOutside: float - Largest percent difference price has moved below this gap 
    daysInside: int - number of days gap has been active 
    active: bool - is fill instance currently active 
    activeAtRisk - is the gap active but price has closed outside of gap 
    entryDate - Date object 
    latestDate - Date object
    highestPercentFill - max percent difference of current price and buttom of gap. Indicates max gain into gap

    """
    def __init__(self,entryPrice,totalFillPercent,top,bottom):
        self.top = top
        self.bottom = bottom
        self.percentFilled = 0
        self.totalFillPercent = totalFillPercent
        self.percentOutside = 0 
        self.daysInside = 0
        self.active = True
        self.minAfterExit = top
        self.entryDate = entryPrice.date
        self.latestDate = entryPrice.date
        self.highestPercentFilled = 0
        self.farthestPrice = bottom
        self.entryPrice = entryPrice 
        self.percentFilledOnEntry = (((entryPrice-self.bottom)/self.bottom)).price/totalFillPercent
    

    def updateFill(self,candle):
        self.latestDate = candle.date

        tempFill = (((candle.high-self.bottom)/self.bottom)).price
        self.percentFilled = max(tempFill,self.percentFilled)

        self.highestPercentFilled = self.percentFilled/self.totalFillPercent
        self.highestPercentFilled = min(self.highestPercentFilled,1)
        self.farthestPrice = max(self.farthestPrice,candle.high)
        
        if (self.farthestPrice > self.top):
            self.farthestPrice = self.top

        if candle.close > self.bottom: 
            self.daysInside = self.daysInside+1
            self.percentOutside = max(self.percentOutside,(((self.bottom-candle.low)/self.bottom)).price)
        else: 
            self.active = False

    def __repr__(self): 
        s = str(round(self.highestPercentFilled*100,4)) + "% Filled " + str(self.minAfterExit)
        # s += "days " + str(self.daysInside)
        # s += "\nLargest Move Out: " + str(self.percentOutside) + "% \n"
        return s        

class GapBelowFill: 
    """
    Class to encapsulate the data points that represent a GapFill below. Price may enter and attempt 
    to fill a gap multiple times. A GapBelowFill object is one of these attempts. It remains active 
    while price closes within the gap or closes outside for a maximum of one day 

    Attribues: 
    top : Price - top of gap
    bottom: Price - buttom of gap
    percentFilled: float - percent gain within gap / total percent size of gap 
    percentOutside: float - Largest percent difference price has moved below this gap 
    daysInside: int - number of days gap has been active 
    active: bool - is fill instance currently active 
    activeAtRisk - is the gap active but price has closed outside of gap 
    entryDate - Date object 
    latestDate - Date object
    highestPercentFill - max percent difference of current price and buttom of gap. Indicates max gain into gap

    """
    def __init__(self,entryPrice,totalFillPercent,top,bottom):
        self.top = top
        self.bottom = bottom
        self.percentFilled = 0
        self.totalFillPercent = totalFillPercent
        self.percentOutside = 0 
        self.daysInside = 0
        self.active = True
        self.maxAfterExit = bottom
        self.entryDate = entryPrice.date
        self.latestDate = entryPrice.date
        self.highestPercentFilled = 0
        self.farthestPrice = top
        self.entryPrice = entryPrice
        self.percentFilledOnEntry = (((self.top-entryPrice)/self.top)).price/totalFillPercent
    
    def updateFill(self,candle):
        self.latestDate = candle.date

        tempFill = (((self.top-candle.low)/self.top)).price
        self.percentFilled = max(tempFill,self.percentFilled)
        
        self.highestPercentFilled = self.percentFilled/self.totalFillPercent
        self.highestPercentFilled = min(self.highestPercentFilled,1)
        self.farthestPrice = min(self.farthestPrice,candle.low)

        if self.farthestPrice < self.bottom: 
            self.farthestPrice = self.bottom

        if candle.close < self.top: 
            self.daysInside = self.daysInside+1
            self.activeAtRisk = False
        else: 
            self.active = False 
            self.percentOutside = max(self.percentOutside,(((candle.high-self.top)/self.top)).price)
    
    def __repr__(self): 
        s = str(round(self.highestPercentFilled*100,4)) + "% Filled " + str(self.maxAfterExit)
        # s += "days " + str(self.daysInside) 
        # s += "\nLargest Move Out: " + str(self.percentOutside) + "% \n"
        return s  

