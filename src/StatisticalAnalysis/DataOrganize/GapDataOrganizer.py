import pandas as pd 
import numpy as np
import openpyxl
import math


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
            "RiskReward":[],
            "PercentFillOnEntry":[],
            "RewardAfterExit":[],
            "Size":[]
        }

        self.belowStopLossDictionary = {
            "GapHighs":[],
            "LowAfterExit":[],
            "RiskReward":[], 
            "PercentFillOnEntry":[],
            "RewardAfterExit":[],
            "Size":[]
        }

        self.aggregateBinsAbove = dict()

        self.aggregateBinsBelow = dict() 


        self.memo = []
        self.gapHighs = [] 
        self.gapLows = []
        self.riskReward = [] 
        self.percentFillOnEntry = []
        self.rewardAfterExit = [] 
    

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
            self.percentFillOnEntry = [] 
            self.rewardAfterExit = [] 
            self.size = [] 

            fillInstances = gap.fillInstances
            if not gap.below: 
                self.stopLossFillAbove(0,len(fillInstances),gap,fillInstances)
                self.aboveStopLossDictionary["Size"] += self.size 
                self.aboveStopLossDictionary["GapHighs"] += self.gapHighs
                self.aboveStopLossDictionary["LowAfterExit"] += self.gapLows
                self.aboveStopLossDictionary["RiskReward"] += self.riskReward
                self.aboveStopLossDictionary["PercentFillOnEntry"] += self.percentFillOnEntry
                self.aboveStopLossDictionary["RewardAfterExit"] += self.rewardAfterExit 
            else: 
                self.stopLossFillBelow(0,len(fillInstances),gap,fillInstances)
                self.belowStopLossDictionary["Size"] += self.size 
                self.belowStopLossDictionary["GapHighs"] += self.gapHighs
                self.belowStopLossDictionary["LowAfterExit"] += self.gapLows
                self.belowStopLossDictionary["RiskReward"] += self.riskReward
                self.belowStopLossDictionary["PercentFillOnEntry"] += self.percentFillOnEntry
                self.belowStopLossDictionary["RewardAfterExit"] += self.rewardAfterExit 

            

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

        self.percentFillOnEntry.append(fillInstances[start].percentFilledOnEntry)
        for index in range(start,end): 
            minVal = min(minVal,fillInstances[index].minAfterExit)
        
        reward = fillInstances[end-1].farthestPrice - fillInstances[start].entryPrice 

        self.size.append(gap.totalFillPercent)
        self.rewardAfterExit.append((reward/fillInstances[start].entryPrice).price/(gap.totalFillPercent))
        risk = gap.bottom - minVal
        self.riskReward.append((risk/reward).price)
        self.gapHighs.append(fillInstances[start].highestPercentFilled)
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

        self.percentFillOnEntry.append(fillInstances[start].percentFilledOnEntry)
        for index in range(start,end): 
            maxVal = max(maxVal,fillInstances[index].maxAfterExit)
        
        reward = fillInstances[start].entryPrice - fillInstances[end-1].farthestPrice  

        self.size.append(gap.totalFillPercent)  
        self.rewardAfterExit.append((reward/fillInstances[start].entryPrice).price/(gap.totalFillPercent))
        risk = maxVal - gap.top
        self.riskReward.append((reward/risk).price)
        self.gapHighs.append(fillInstances[start].highestPercentFilled)
        self.gapLows.append(((((risk)/gap.top))).price/(gap.totalFillPercent)*100)

        self.stopLossFillBelow(start,end-1,gap,fillInstances)
        self.stopLossFillBelow(start+1,end,gap,fillInstances)

    def aggregateBins(self,step,binMethodToCall):
        for i in np.arange(step,100+step,step): 
            self.aggregateBinsAbove[i] = (0,0)
            self.aggregateBinsBelow[i] = (0,0)
        

        lowAfterExit = self.aboveStopLossDictionary["LowAfterExit"]


        totalPatterns = 0
        for index in range(0,len(lowAfterExit)):

            curLow = lowAfterExit[index] 
            for key in self.aggregateBinsAbove: 
                if curLow != 0: 
                    binMethodToCall(key,index,curLow)

        # if binMethodToCall == self.aggregateByPL:
        #     totalPatterns = len(lowAfterExit)
        #     for key in self.aggregateBinsAbove: 
        #         temp = self.aggregateBinsAbove[key]
        #         patternsExcluded = len(lowAfterExit) - temp[0]
        #         print(patternsExcluded)
        #         stoppedOutValue = patternsExcluded * key
        #         self.aggregateBinsAbove[key] = temp[1] - stoppedOutValue
        # else: 
        for key in self.aggregateBinsAbove:
            tup = self.aggregateBinsAbove[key]
            self.aggregateBinsAbove[key] = tup[1]
            

        
            
    def aggregateByRR(self,binKey, patternIndex,curlow): 
        if curlow < binKey:   
            rewardAfterExit = self.aboveStopLossDictionary["RewardAfterExit"]
            temp = self.aggregateBinsAbove[binKey]
                                
                        
            count = temp[0]
            avg = temp[1]
            newSum = (avg*count)+(rewardAfterExit[patternIndex]/curlow)
            # print(rewardAfterExit[index])
            # print(key/self.rewardAfterExit[index])
            # print(temp)
            self.aggregateBinsAbove[binKey] = (count+1,(newSum)/(count+1))

            # print(self.aggregateBinsAbove[key])
            # print("\n")
    
    def aggregateByPL(self,binKey, patternIndex,curlow):   
        size = self.aboveStopLossDictionary["Size"][patternIndex]
        temp = self.aggregateBinsAbove[binKey]
        if curlow < binKey: 
            rewardAfterExit = self.aboveStopLossDictionary["RewardAfterExit"][patternIndex]
            

            reward = rewardAfterExit*size * 100
            profit = temp[1] + reward

            self.aggregateBinsAbove[binKey] = (temp[0]+1,profit)
        else: 

            risk = binKey/100 * size * 100
            loss = temp[1] - risk
            self.aggregateBinsAbove[binKey] = (temp[0]+1,loss)


    

    def saveToExcel(self): 
        dataFrameAbove = pd.DataFrame.from_dict(self.aboveStopLossDictionary)
        dataFrameAbove.to_excel('SavedData/gapDataAbove.xlsx')

        dataFrameBelow = pd.DataFrame.from_dict(self.belowStopLossDictionary)
        dataFrameBelow.to_excel('SavedData/gapDataBelow.xlsx')

        dataFrameAbove = pd.DataFrame(self.aggregateBinsAbove,index = [1])
        dataFrameAbove = dataFrameAbove.T
        dataFrameAbove.to_excel('SavedData/AggregateDataAbove.xlsx')


    
    



    

        



