
import DataCollection.Stock as Stock
import DataCollection.ImportData as ImportData
import PriceAnalysis.FindPatterns as Patterns
import StatisticalAnalysis.DataOrganize.GapDataOrganizer as GapDataOrganizer
import StatisticalAnalysis.DataOrganize.GapDataOrganize2 as GapDataOrganizer2
import app
import plotly.express as px
import plotly.graph_objects as go



'''
run this file to generate data set and analyze it.
At this time this program is in its earliest stages.
(will update) it currently only generates support and resistance 
and the app will display the support and resistance along with the price data. 
'''
def main(): 

    importDataObject = ImportData.CreateDataSet()
    
    importDataObject = initializeDataSet(importDataObject)

    stockDict = importDataObject.returnData()

    # for key in stockDict: 
    #     print(stockDict[key].gapContainer.archivedGaps)

    startDate = '2018-01-01'

    stockDict = analyzeStocks(stockDict,startDate)

    importDataObject.writeData(stockDict)

    organizer = GapDataOrganizer2.GapDataOrganizer(stockDict)

    organizer.organizeData()
    organizer.aggregateBins(5) 
    organizer.saveToExcel() 

    print(organizer.gapAbovePositions)


    # print(organizer.stopLossDictionary)

    # gapDictionary = organizer.aboveStopLossDictionary

    # organizer.aggregateBins(2.5,organizer.aggregateByPL)

    # organizer.saveToExcel()

    # fig = px.scatter_3d(gapDictionary,x = 'GapHighs',y = 'LowAfterExit',z = 'RiskReward')
    # fig.update_layout(
    # scene = dict(
    #     xaxis = dict(nticks=4, range=[0,100],),
    #                  yaxis = dict(nticks=4, range=[0,100],),
    #                  zaxis = dict(nticks=4, range=[-5,5],),),
    # width=700,
    # margin=dict(r=20, l=10, b=10, t=10))

    # fig.show()


    # importDataObject.writeData(stockDict)

    # app.createApp(stockDict)

'''
Initialize the dataset. The importData classes are set up 
to download and create pickle file of all stocks to be analyzed. 
If a pickle file already exists, nothing will be downloaded
'''        
def initializeDataSet(importDataObject):
    tickers = importDataObject.generateTickers()
    importDataObject.addTickers(tickers)

    importDataObject.clearBadTicks()
    return importDataObject

'''
This will loop through every stock in the data set and analyze the price data.
At this point it only generate support and resistance, the basis of all chart patterns
This process is EXTREMELY slow but only needs to be done once.
'''
def analyzeStocks(stockDict,startDate):
    
    stockDictCopy = stockDict.copy()
    for stock in stockDict.keys():
        if not stockDict.get(stock).gapContainer == None:
            continue
        patternFinder = Patterns.FindPatterns(stockDict.get(stock))
        
        patternFinder.analyzePriceData(startDate)
        
        stockDictCopy[stock] = patternFinder.returnStock()
        print(stock)


    return stockDictCopy

main() 

def gapTest(): 
    startDate = '2020-03-05'
    testStock = Stock.StockObject("LUMN")
    testStock.initializeDataInRange(startDate,'2021-01-27')
    # testStock.initializeData('2000-01-01')
    PatternFinder = Patterns.FindPatterns(testStock)
    PatternFinder.analyzePriceData('2020-03-05') 
    stockDictionary = {"LUMN": PatternFinder.returnStock()}

    print(stockDictionary['LUMN'].gapContainer.archivedGaps)
    organizer = GapDataOrganizer2.GapDataOrganizer(stockDictionary)

    organizer.organizeData()
    organizer.aggregateBins(5) 
    organizer.saveToExcel() 


    
    # organizer.aggregateBins(2.5)
    # organizer.saveToExcel()
    # print(organizer.aboveStopLossDictionary)

    # print(organizer.aggregateBinsAbove)

    print(organizer.gapAbovePositions)
    # print(organizer.aboveStopLossDictionary)


    # gapDictionary = organizer.aboveStopLossDictionary

    

    # fig = px.scatter_3d(gapDictionary,x = 'GapHighs',y = 'LowAfterExit',z = 'RiskReward')
    # fig.show()
    


# gapTest()