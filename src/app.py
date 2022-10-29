
from tkinter import CENTER
import plotly.graph_objects as go
import DataCollection.ImportData as ImportData
from dash import Dash, dcc,Output,Input
import dash_bootstrap_components as dbc 

def createApp(stockDict):
    
    stockTickers = []
    for stock in stockDict.keys():
        stockTickers += [stock]

    app = Dash(__name__)
    mytitle = dcc.Markdown(children='Chart With Generated Support and Resistance Levels',style = {'font-size': 29,'text-align':CENTER})
    descript = dcc.Markdown(children= 'Display generated support and resistance levels for '
     'each stock in the drop down menu. Currently the view is a work in progress make use of the zoom feature '
     'to zoom to any "box" you select on the chart. Additionally old support and resistance lines clutter'
     'the current view but will be updated.')
    mygraph = dcc.Graph(figure ={})
    dropdown = dcc.Dropdown(options=stockTickers,
                            value = 'AAPL',
                            clearable = False)

    app.layout = dbc.Container([mytitle,dropdown,descript,mygraph])

    @app.callback(
        Output(mygraph,component_property='figure'),
        Input(dropdown,component_property='value')
    )

    def update_graph(stock_ticker):

        stock = stockDict.get(stock_ticker)
        priceData = stock.priceData

        figure = go.Figure(data=[go.Candlestick(x = priceData.index,
        open = priceData['Open'], high = priceData['High'],
        low = priceData['Low'], close = priceData['Close'])
        ])
        figure.update_layout(height = 700)
        figure.update_yaxes(autorange=True)
        figure.update_yaxes(fixedrange=False)

        levels = stock.levels
        for level in levels:
            if level.getTotalTouches() < 3:
                continue
            figure.add_hline(y=level.price.price)
        

        return figure



    app.run(debug=True)