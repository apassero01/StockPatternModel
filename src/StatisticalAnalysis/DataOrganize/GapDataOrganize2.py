import pandas as pd 
import numpy as np 
import statistics
import PriceAnalysis.Patterns.Patterns as patterns



class GapDataOrganizer: 

    #When simulatign positions, $100 position is used for each gap position 
    TEST_POSITION_SIZE = 100 

    def __init__(self,stockDictionary):
        self.stockDictionary = stockDictionary
        self.gapAbovePositions = [] 
        self.gapBelowPositions = []

        self.aggregateBinsAbove = dict() 
        self.aggregateBinsBelow = dict() 

        self.avgCutOff = 0
        self.total = 0

    
    def organizeData(self):
        for ticker in self.stockDictionary.keys(): 
            stock = self.stockDictionary[ticker]
            gapContainer = stock.gapContainer

            for gap in gapContainer.archivedGaps: 
                if not gap.below: 
                    abovePosition = GapAbovePosition(gap,ticker)
                    if not abovePosition.validPosition: 
                        continue
                    abovePosition.analyzePositions()
                    if not abovePosition.validPosition: 
                        continue
                    self.gapAbovePositions.append(abovePosition)

    

    def aggregateBins(self,step):
        binSize = 150
        for i in np.arange(step,binSize+step,step):
            self.aggregateBinsAbove[i] = (0,0,0)
            self.aggregateBinsBelow[i] = (0,0,0)
        
        for i in range(len(self.gapAbovePositions)):
            position = self.gapAbovePositions[i]
            percentReward = position.percentReward
            neverFilled = False 


            if (percentReward == 0): 
                neverFilled = True 
            

            lastBin = 0 
            for ranges in position.cutOffRanges: 
                timesStoppedOut = 0 
                for cutOff in position.orderedCutOffs: 
                    if cutOff >= ranges[1]: 
                        timesStoppedOut += 1
                
                for bin in self.aggregateBinsAbove: 
                    if bin/100 > ranges[1]:
                        timesStoppedOut = 0
                        lastBin = bin 
                        break
                    if bin < lastBin:
                        continue
                    
                    if bin/100 * position.size < .02: 
                        loss = .02 * self.TEST_POSITION_SIZE * timesStoppedOut
                    else: 
                        loss = bin/100 * position.size * self.TEST_POSITION_SIZE * timesStoppedOut
                    oldVal = self.aggregateBinsAbove[bin]
                    self.aggregateBinsAbove[bin] = (oldVal[0]-loss,oldVal[1]+timesStoppedOut,oldVal[2])

                    # if not neverFilled: 
                    #     profit = percentReward * self.TEST_POSITION_SIZE
                    #     oldVal = self.aggregateBinsAbove[bin]
                    #     self.aggregateBinsAbove[bin] = (oldVal[0]+profit,oldVal[1],oldVal[2]+1)
                if bin == binSize: 
                    break

            for bin in self.aggregateBinsAbove:
                profit = percentReward * self.TEST_POSITION_SIZE
                oldVal = self.aggregateBinsAbove[bin]
                self.aggregateBinsAbove[bin] = (oldVal[0]+profit,oldVal[1],oldVal[2]+1)


    def saveToExcel(self):
        dataFrameAbove = pd.DataFrame(self.aggregateBinsAbove)
        dataFrameAbove = dataFrameAbove.T
        dataFrameAbove.to_excel('SavedData/AggregateDataAbove.xlsx')      
                    


class GapAbovePosition: 
    '''
    Class responsible for organizing gap fill attemps chronologically to determine positional outcome 
    based on stop stop losses and price targets
    '''

    PERCENT_FILL_TARGET = .75
    INITIAL_FILL_ENTRY_THRESH = .2

    def __init__(self, gapAbove,ticker): 
        self.ticker = ticker 
        self.gapAbove = gapAbove
        self.size = self.gapAbove.totalFillPercent
        self.fillInstances = gapAbove.fillInstances

        self.allEntryPrices = [] 
        self.orderedCutOffs = [] 
        self.cutOffRanges = [] 
        self.fillsToTarget = 0 

        self.avgEntryPrice = 0
 
            
        if len(self.fillInstances) != 0:
            self.initialFill = self.fillInstances[0]
            entryPrice = self.initialFill.entryPrice

            self.allEntryPrices.append(entryPrice.price)

            self.percentFilledOnEntry = self.initialFill.percentFilledOnEntry
            self.initialHighestPercentFilled = self.initialFill.highestPercentFilled 

            #If we want to know the percent gain on an investment with a price target of 75% of the total gap, the below equation gives the percent gain target
            self.percentGainTarget = self.PERCENT_FILL_TARGET * gapAbove.totalFillPercent 

            #Reversing the percent change equation to solve for final price knowing our percentGainTarget, we fer price target
            self.priceTarget = (self.gapAbove.bottom.price*self.percentGainTarget) + self.gapAbove.bottom.price


            self.validPosition = True 
        else: 
            self.validPosition = False 

        
        
    
    def analyzePositions(self):
        self.targetHit = False 
        self.percentReward = 0  
        self.percentRisk = 0 

        #Logic for if the gap was filled on the initial fill 
        if self.initialHighestPercentFilled > self.PERCENT_FILL_TARGET: 
            minimum = self.initialFill.minPrice
            
            entryPrice = self.allEntryPrices[0]
            self.percentReward = (self.priceTarget - entryPrice)/entryPrice
            self.percentRisk = ((patterns.Price(entryPrice) - minimum)/patterns.Price(entryPrice)).price 
            rewardCutOff = round(self.percentRisk/self.gapAbove.totalFillPercent,2) 

            rewardCutOff = max(0,rewardCutOff)
            self.orderedCutOffs += [rewardCutOff]

            self.targetHit = True 

            self.fillsToTarget = 1

            if self.percentFilledOnEntry > self.INITIAL_FILL_ENTRY_THRESH:
                self.validPosition = False 
                
        
        
        else:

            #Logic for if the gap has only one fill instance but has not been filled yet 
            if len(self.fillInstances) < 2: 
                minAfterExit = self.initialFill.minAfterExit 
                minimum = self.initialFill.minPrice

                if minAfterExit > self.gapAbove.bottom: 
                    self.validPosition = False 

                minimum = min(minimum,minAfterExit)
                self.percentRisk = ((self.gapAbove.bottom - minimum)/self.gapAbove.bottom).price 

                rewardCutOff = round(self.percentRisk/self.gapAbove.totalFillPercent,2)

                self.orderedCutOffs += [rewardCutOff]
                 
            else: 
                minAfterExit = self.gapAbove.top


                for index in range(1,len(self.fillInstances)): 
                    fill = self.fillInstances[index]
                    highestPercentFilled = fill.highestPercentFilled
                    
                    minAfterExit = min(minAfterExit,self.fillInstances[index-1].minAfterExit)

                    curMin = self.fillInstances[index-1].minAfterExit

                    curMin = min(curMin,fill.minPrice)

                    prevEntry = patterns.Price(self.allEntryPrices[len(self.allEntryPrices)-1])
                    self.percentRisk = ((prevEntry - curMin)/prevEntry).price 
                    rewardCutOff = round(self.percentRisk/self.gapAbove.totalFillPercent,2)

                    self.orderedCutOffs += [rewardCutOff]
                    self.allEntryPrices.append(fill.entryPrice.price)



                    if highestPercentFilled > self.PERCENT_FILL_TARGET: 
                        
                        self.avgEntryPrice = statistics.mean(self.allEntryPrices)
                        self.percentReward = (self.priceTarget - self.avgEntryPrice)/self.avgEntryPrice
                        self.targetHit = True
                        self.fillsToTarget = index + 1  
                        break 


                if not self.targetHit: 
                    curMin = self.fillInstances[len(self.fillInstances)-1].minAfterExit
                    if minAfterExit > self.gapAbove.bottom: 
                        self.validPosition = False 
                    self.percentRisk = ((self.gapAbove.bottom - curMin)/self.gapAbove.bottom).price 
                    rewardCutOff = round(self.percentRisk/self.gapAbove.totalFillPercent,2)
                    self.orderedCutOffs += [rewardCutOff]
            
        cutOffsSorted = self.orderedCutOffs.copy() 
        cutOffsSorted.sort() 


        self.cutOffRanges.append((0,cutOffsSorted[0]))
        for index in range(1,len(cutOffsSorted)):
            self.cutOffRanges.append((self.cutOffRanges[index-1][1],cutOffsSorted[index]))

            
    def __repr__(self): 
        s = "\n" + str(round(self.size*100,2))+"% " + "Gap Above, Stock: " + self.ticker + "\n"
        s+="Date: " + self.gapAbove.top.date.strftime("%m/%d/%Y") + "\n"
        s+="Reward: " + str(round(self.percentReward*100,2)) + "%\n"
        # s+="Risk: " + str(round(self.percentRisk*100,2)) + "%\n"
        s+= "rewardCutOffs: " + str(self.orderedCutOffs) + " \n"
        s+= "CutOfRanges " +  str(self.cutOffRanges) + "\n"
        s+= "Filled on the " + str(self.fillsToTarget) + " fill attempt \n"
        s+= "TargetHit? " + str(self.targetHit) + " \n"
        return s

        


