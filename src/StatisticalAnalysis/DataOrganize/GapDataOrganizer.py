import pandas as pd 
import openpyxl


class GapDataOrganizer: 
    '''
    Class responsible for organizing GapFill data. Creates a dictionary of the various measureables of 
    all gapFill instances and can write them to an xlxs file for further analysis
    '''
    def __init__(self,stockDictionary): 
        self.stockDictionary = stockDictionary
        self.aboveStopLossDictionary = {
            "GapHighs":[],
            "LowAfterExit":[],
            "RiskReward":[] 
        }

        self.belowStopLossDictionary = {
            "GapHighs":[],
            "LowAfterExit":[],
            "RiskReward":[] 
        }

        self.memo = []
        self.gapHighs = [] 
        self.gapLows = []
        self.riskReward = [] 
    

    def organizeData(self): 
        for stock in self.stockDictionary.keys(): 
            self.stopLossAnalysis(self.stockDictionary[stock])

    def stopLossAnalysis(self,stock):
        '''
        Method to loop through all gaps and perform analysis
        ''' 
        gapContainer = stock.gapContainer

        # if (stock.ticker == "CME"):
        
        #     print("CME")
        
        gaps = gapContainer.archivedGaps

        for gap in gaps: 
            self.memo = [] 
            self.gapHighs = [] 
            self.gapLows = [] 
            self.riskReward = []

            fillInstances = gap.fillInstances
            if not gap.below: 
                self.stopLossFillAbove(0,len(fillInstances),gap,fillInstances)
                self.aboveStopLossDictionary["GapHighs"] += self.gapHighs
                self.aboveStopLossDictionary["LowAfterExit"] += self.gapLows
                self.aboveStopLossDictionary["RiskReward"] += self.riskReward
            else: 
                self.stopLossFillBelow(0,len(fillInstances),gap,fillInstances)
                self.belowStopLossDictionary["GapHighs"] += self.gapHighs
                self.belowStopLossDictionary["LowAfterExit"] += self.gapLows
                self.belowStopLossDictionary["RiskReward"] += self.riskReward

            

    def stopLossFillAbove(self,start, end,gap,fillInstances): 
        '''
        Recursive function to calculate risk/reward and farthestPrice away between gapfill instances. For a gap containing multiple gapFills 
        all in chronological order, there is an associated risk/reward and farthestPriceAway point between any two fill instances in a gap. This method
        calculates and stores r/r & farthestPriceAway for every pair of fill instances. The farthestPriceAway point between two non consecutive fills in 
        the fillInstances list may exist within the fill objects in between the two objects in the list. Therefore, this method loops through all fills
        between start and end finding farthestAway price and then calculating risk/reward. 

        '''
        if abs(start-end) <= 1 or (start,end) in self.memo: 
            return
        
        self.memo.append((start,end))
        minVal = gap.top
        for index in range(start,end): 
            minVal = min(minVal,fillInstances[index].minAfterExit)
        
        reward = fillInstances[end-1].farthestPrice - fillInstances[start].farthestPrice 
        risk = gap.bottom - minVal
        self.riskReward.append((reward/risk).price)
        self.gapHighs.append(fillInstances[start].highestPercentFilled*100)
        self.gapLows.append(((((gap.bottom - minVal)/gap.bottom))).price/(gap.totalFillPercent)*100)

        self.stopLossFillAbove(start,end-1,gap,fillInstances)
        self.stopLossFillAbove(start+1,end,gap,fillInstances)
    

    def stopLossFillBelow(self,start, end,gap,fillInstances): 
        '''
        Recursive function to calculate risk/reward and farthestPrice away between gapfill instances. For a gap containing multiple gapFills 
        all in chronological order, there is an associated risk/reward and farthestPriceAway point between any two fill instances in a gap. This method
        calculates and stores r/r & farthestPriceAway for every pair of fill instances. The farthestPriceAway point between two non consecutive fills in 
        the fillInstances list may exist within the fill objects in between the two objects in the list. Therefore, this method loops through all fills
        between start and end finding farthestAway price and then calculating risk/reward. 

        '''
        if abs(start-end) <= 1 or (start,end) in self.memo: 
            return
        
        self.memo.append((start,end))
        maxVal = gap.bottom
        for index in range(start,end): 
            maxVal = max(maxVal,fillInstances[index].maxAfterExit)
        
        reward = fillInstances[end-1].farthestPrice - fillInstances[start].farthestPrice 
        risk = maxVal - gap.top
        self.riskReward.append((reward/risk).price)
        self.gapHighs.append(fillInstances[start].highestPercentFilled*100)
        self.gapLows.append(((((risk)/gap.top))).price/(gap.totalFillPercent)*100)

        self.stopLossFillBelow(start,end-1,gap,fillInstances)
        self.stopLossFillBelow(start+1,end,gap,fillInstances)

    def saveToExcel(self): 
        dataFrameAbove = pd.DataFrame.from_dict(self.aboveStopLossDictionary)
        dataFrameAbove.to_excel('SavedData/gapDataAbove.xlsx')

        dataFrameBelow = pd.DataFrame.from_dict(self.belowStopLossDictionary)
        dataFrameBelow.to_excel('SavedData/gapDataBelow.xlsx')
    
    



    

        



