import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/InternetPrices.csv')
df2 = pd.read_csv('../Datasets/PowerPrices.csv')

app = dash.Dash()

# Bar chart data for internet providers
barchart_df = df1
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.sort_values(by=['Price'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['Company&Plan'], y=barchart_df['Price'])]

# Bar chart data for power providers
barchart_df = df2
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.sort_values(by=['Price'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['Company'], y=barchart_df['Price'])]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Internet Prices In My Local Area -  5/9/2021', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the prices per month of the internet providers in my area. You can use the button below to switch to bundle prices.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a Price type.', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-type',
        options=[
            {'label': 'Internet Only', 'value': 'Internet'},
            {'label': 'Internet And TV', 'value': 'Internet/TV'},
            {'label': 'Internet, TV, and Calls', 'value': 'Internet/TV/Calls'}
        ],
        value='Internet'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the cost of power services in my area.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Power Company Prices',
                                      xaxis={'title': 'Companies'}, yaxis={'title': 'Price per Month ($)'})
              }
              )

])


@app.callback(Output('graph1', 'figure'),
              [Input('select-type', 'value')])
def update_figure(selected_type):
    filtered_df = df1[df1['Type'] == selected_type]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['Company&Plan'])['Price'].sum().reset_index()
    new_df = new_df.sort_values(by=['Price'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['Company&Plan'], y=new_df['Price'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Internet Prices per Company',
                                                                   xaxis={'title': 'Company & Plan'},
                                                                   yaxis={'title': 'Price per Month ($)'})}


if __name__ == '__main__':
    app.run_server()
