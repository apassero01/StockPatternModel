# StockPattern Predictive Model
This program is a work in progress with the goal of using historical stock data to identify patterns and analyze the statistics related to these patterns in order to make a predictive model. 

It currently only analyzes for support and resistance. In the future the analysis algorithms will be better optimized for faster runntime.

The algorithm will add detection of patterns one pattern at a time. The graph will be updated to demonstrate the patterns as they are added.

Once Patterns begin to be identified with high accuracy, algorithms to statistically analyze all occurances of each pattern will be added. 



## HowTo: 
1. Once this repository is cloned, install all libraries in requirements.txt 
2. Run the main file 
    -   The first time the program is run, all historical price data from the S&P500 will be downloaded and saved to a .pickle file
    -   Additionally on the initial run of the program, the analysis algorithm will run. IT IS SLOW FOR NOW. it is a work in progress,
    the algorithm is O(n) however there are a lot of data points and the wrapping of objects slows the runntime. This will be updated for
    better optimization in the future. 
3. there should be a local address printed in the console that will open in a web browser. This will show the price data for whichever stock is selected along with the support and resistance levels 


## Example image of AAPL support and resistance in application 
