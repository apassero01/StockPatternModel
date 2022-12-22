import bisect 
from PriceAnalysis.Patterns import GapBelow,GapAbove

'''
Class with functionality to store all gap instances for a specific stock.
Contains a list for gapAboves and gapBelows that are sorted such that the first 
element contains the gap that is closest to the current price. 
'''
class GapContainer:
    def __init__(self):
        self.gapsAbove = []
        self.gapsBelow = [] 
        self.activeGapAbove = None
        self.activeGapBelow = None 
        self.archivedGaps = []
    
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
    def analyzeGaps(self,currentPrice): 


        ##Analyze active gaps above and check for closest gapAbove
        if self.activeGapAbove != None: 
            self.activeGapAbove.updateGap(currentPrice)
            if self.activeGapAbove.filled == True:
                self.gapsAbove.remove(self.activeGapAbove)
                self.activeGapAbove == None
            if not self.activeGapAbove.inside:
                self.activeGapAbove == None

        if len(self.gapsAbove) > 0:
            self.closestAbove = self.gapsAbove[0]
            self.closestAbove.updateGap(currentPrice)
            if self.closestAbove.inside: 
                self.activeGapAbove = self.closestAbove

        ##Analyze active gaps below and check for closest gapBelow
        if self.activeGapBelow != None: 
            self.activeGapBelow.updateGap(currentPrice)
            if self.activeGapBelow.filled == True:
                self.gapsBelow.remove(self.activeGapBelow)
                self.activeGapBelow == None
            if not self.activeGapBelow.inside:
                self.activeGapBelow == None
        
        if len(self.gapsBelow) > 0 :
            self.closestBelow = self.gapsBelow[0]
            self.closestBelow.updateGap(currentPrice)
            if self.closestBelow.inside: 
                self.activeGapBelow = self.closestBelow


        
    
