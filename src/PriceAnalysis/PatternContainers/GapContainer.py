import bisect 
import sys
from PriceAnalysis.Patterns.GapPattern import GapBelow,GapAbove

'''
Class with functionality to store all gap instances for a specific stock.
Contains a list for gapAboves and gapBelows that are sorted such that the first 
element contains the gap that is closest to the current price. 
'''
class GapContainer:
    def __init__(self,minPrice,maxPrice):
        self.gapsAbove = []
        self.gapsBelow = [] 
        self.activeGapAbove = None
        self.activeGapBelow = None 
        self.archivedGaps = []
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        
    
    '''
    Method to add a gap to the stocks gap container. Determines if the gap is below or above
    and adds it to correct list in correct order. 
    percentChange - size of the gap calculated in @checkForGap in FindPatterns
    periodOpen - opening price of current period 
    periodClose - closing price of previos period.

    '''
    def addGap(self,periodOpen, prevClose, percentChange):
        gap = None; 
        if percentChange > 0: 
            gap = GapBelow(periodOpen,prevClose)
            bisect.insort(self.gapsBelow,gap)
        else: 
            gap = GapAbove(prevClose,periodOpen)
            bisect.insort(self.gapsAbove,gap)
        self.archivedGaps += [gap]


    '''
    Method for analzying all exisiting gaps given the current price. 
    '''    
    def analyzeGaps(self,candle): 


        ##Analyze active gaps above and check for closest gapAbove

        if len(self.gapsAbove) > 0:
            self.closestAbove = self.gapsAbove[0]
            self.closestAbove.updateGap(candle)
            self.minPrice = min(self.minPrice,candle.low)
            if self.closestAbove.newFill: 
                for i in range(0,len(self.gapsAbove)):
                    if len(self.gapsAbove[i].fillInstances) > 0: 
                        self.gapsAbove[i].setNewMin(self.minPrice)
                self.minPrice = self.closestAbove.top
            if self.closestAbove.inside: 
                if self.closestAbove.filled: 
                    self.gapsAbove.remove(self.closestAbove)
                    self.closestAbove = None

        ##Analyze active gaps below and check for closest gapBelow
        
        if len(self.gapsBelow) > 0:
            self.maxPrice = max(self.maxPrice,candle.high)
            self.closestBelow = self.gapsBelow[0]
            self.closestBelow.updateGap(candle)
            if self.closestBelow.newFill:
                for i in range(0,len(self.gapsBelow)):
                    if len(self.gapsBelow[i].fillInstances) > 0:
                        self.gapsBelow[i].setNewMax(self.maxPrice)
                self.maxPrice = self.closestBelow.bottom
            if self.closestBelow.inside: 
                if self.closestBelow.filled: 
                    self.gapsBelow.remove(self.closestBelow)
                    self.closestBelow = None


        
    
