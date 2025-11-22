from dash import Dash, html, dcc, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)
app.layout = html.Div([
    html.H4('Stock candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Dropdown(
        id='dropdownFileDrop',
        options=[
            {'label': 'FFC', 'value': './csv/FFC.csv'},
            {'label': 'LUCK', 'value': './csv/LUCK.csv'},
            {'label': 'OGDC', 'value': './csv/OGDC.csv'}
        ],
        placeholder='select the file',        
        value='./csv/FFC.csv'
    ),
    dcc.Graph(id="graph"),
    
])


@app.callback(
    Output("graph", "figure"),
    Input("toggle-rangeslider", "value"),
    Input("dropdownFileDrop", "value"))


def display_candlestick(value, selectedFile):    
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv') # replace with your own data source

    dfRead = pd.read_csv(selectedFile)  # replace with your own data source
    df = dfRead.sort_values('Date')

    dfMean  = df;

    dfMean['SMA5']   = df['Close'].rolling(window=5).mean();
    dfMean['SMA15']  = df['Close'].rolling(window=15).mean();
    dfMean['SMA30']  = df['Close'].rolling(window=30).mean();
    dfMean['SMA50']  = df['Close'].rolling(window=50).mean();
    dfMean['SMA100'] = df['Close'].rolling(window=100).mean();    
    dfMean['SMA200'] = df['Close'].rolling(window=200).mean();
    
    
    # print(df)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.03)
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick'
    )
    , row=1, col=1  )

    fig.add_trace(go.Scatter(x=dfMean['Date'], y=dfMean['SMA5'],   mode='lines', name='SMA5'  ) ,
                  row=2, col=1 )
    fig.add_trace(go.Scatter(x=dfMean['Date'], y=dfMean['SMA50'],   mode='lines', name='SMA50'  ),
                  row=2, col=1 )
    fig.add_trace(go.Scatter(x=dfMean['Date'], y=dfMean['SMA100'],   mode='lines', name='SMA200'  ),
                  row=2, col=1 )

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value ,               
           height=800
    )

    return fig
    

app.run(debug=True)