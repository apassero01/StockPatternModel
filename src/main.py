
import DataCollection.Stock as Stock
import DataCollection.ImportData as ImportData
import PriceAnalysis.FindPatterns as Patterns
import app



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

    stockDict = analyzeStocks(stockDict)

    importDataObject.writeData(stockDict)

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
def analyzeStocks(stockDict):
    
    stockDictCopy = stockDict.copy()
    for stock in stockDict.keys():
        patternFinder = Patterns.FindPatterns(stockDict.get(stock))
        patternFinder.analyzePriceData()
        stockDictCopy[stock] = patternFinder.returnStock()
        print(stock)


    return stockDictCopy

main() 

def gapTest(): 
    testStock = Stock.StockObject("LUMN")
    # testStock.initializeDataInRange('2022-02-08','2022-05-31')
    testStock.initializeData('2000-01-01')
    PatternFinder = Patterns.FindPatterns(testStock)
    PatternFinder.analyzePriceData()
    print(PatternFinder.gapContainer.archivedGaps)

# gapTest()