"""
File: 07_dashboard.py
Description: webpage runner that shows the study of the data.
"""

# Import the main libraries
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

data = pd.DataFrame({
    'country': ['USA', 'Canada', 'Mexico', 'Italy'],
    'value': [10, 20, 30, 40]
})

# Creating the dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.H1('Natural gas imports and exports'), # Title of the webpage
    html.Div(id='df_total', style={'display': 'none'}), # Content of the webpage
    dcc.Tabs(id='tabs', value='tab-1', children=[ # Container of tabs
        dcc.Tab(label='Natural gas data analysis', children=[ # First tab - Data analysis
            html.Div(children=[
                html.H2("Natural gas data analysis"), # Subtitle
                html.Div(children=[ # Divide the webpage in 2 columns
                    html.Div(children=[ # First column
                        dcc.Graph(id="world-map", config={'scrollZoom': False})
                    ], style={'width': '70%', 'display': 'inline-block'}),
                    html.Div(children=[ # Second column
                        html.Div(id='output_country')
                    ], style={'width': '30%', 'display': 'inline-block'})
                ])
            ])
        ]),

        dcc.Tab(label='Natural gas autocorrelation', children=[ # Second tab - Autocorrelation
            html.Div([
                html.H2("Natural gas autocorrelation"),
                html.P('CIAO'),
            ])
        ]),

        dcc.Tab(label='Features correlation', children=[ # Third tab - Features correlation
            html.Div([
                html.H2("Features correlation"),
                html.P('BLABLA'),
            ])
        ]),

        dcc.Tab(label='Covid-19', children=[ # Fourth tab - Covid19
            html.Div([
                html.H2("Covid-19 impact"),
                html.P('aiuto il coviddi'),
            ])
        ]),

        dcc.Tab(label='Russo-Ukrainian War', children=[ # Fifth tab - Russo-Ukrainian War
            html.Div([
                html.H2("Russo-Ukrainian War impact"),
                html.P('che merda Putin'),
            ])
        ])

        # We could put a sixth tab if the gas data are well autocorrelated, doing the forecast for the next years

    ])
])


# Callback to update information when a country is clicked
@app.callback(
    Output('output_country', 'children'),
    [Input('world-map', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        country = clickData['points'][0]['location']
        value = data[data['country'] == country]['value'].values[0]
        return f'You clicked on {country}. Value: {value}'
    else:
        return 'Click on a country to see details.'

# App to be able to click in the map
@app.callback(
    Output('world-map', 'figure'),
    [Input('world-map', 'clickData')]
)
def update_map(clickData):
    return {
        'data': [go.Choropleth(
            locations=data['country'],
            z=data['value'],
            locationmode='country names',
            text=data['country'],
            colorscale='Viridis',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix='',
            colorbar_title='Value',
            hoverinfo='text'
        )],
        'layout': go.Layout(
            title='Select two countries',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
    }


if __name__ == '__main__':
    app.run_server(debug = True)