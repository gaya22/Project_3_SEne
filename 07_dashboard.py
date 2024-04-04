"""
File: 07_dashboard.py
Description: webpage runner that shows the study of the data.
"""

# Import the main libraries
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import auxiliary_functions as af

# Load and prepare dataframes
orig_df = pd.read_csv("GTF_export_cleaned.csv")
tot_flows = af.countries_tot_flows(orig_df) # Dataframe with all af the countries (as index) and the total exit/enter flows of the whole period
exit_flow_countries = af.get_exit_countries(orig_df) # List of all the countries involved in the study that have extit flows
enter_flow_countries = af.get_enter_countries(orig_df) # list of all the countries involved in the study that have entry flows

# Creating the dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Creating the layout of the dashboard
app.layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.H1('Natural gas imports and exports'), # Title of the webpage
    html.Div(id='df_total', style={'display': 'none'}), # Content of the webpage
    dcc.Tabs(id='tabs', value='tab-1', children=[ # Container of tabs
        dcc.Tab(label='Natural gas data analysis', children=[ # First tab - Data analysis
            html.Div(children=[
                html.H2("Natural gas data analysis"), # Subtitle
                html.Div(children=[ # Divide the webpage in 2 columns
                    html.Div(children=[ # First column
                        dcc.Graph(id="world-map", 
                                  config={'scrollZoom': True},
                                  clickData={'points': []},
                                  style={'width':'100%', 'height':'80vh'}),
                    ], style={'width': '60%', 'display': 'inline-block'}),
                    html.Div(children=[ # Second column
                        html.Div(id='selected_countries')
                        ], style={'width': '30%', 'display': 'inline-block'}
                    )
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

# App to be able to click in the map
@app.callback(
    Output('world-map', 'figure'),
    [Input('world-map', 'clickData')]
)
def update_map(clickData):
    print("Click data:", clickData)
    selected_countries = [point['location'] for point in clickData['points']]
    print("Selected countries:", selected_countries)
    return {
        'data': [go.Choropleth(
            locations=tot_flows.index,
            z=tot_flows["tot_exit_flows"], # The color of the map is based on the exit flows
            locationmode='country names',
            text=tot_flows.index,
            colorscale='Viridis',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix='',
            colorbar_title='Value',
            hoverinfo='text',
            selectedpoints = selected_countries
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

# Callback to update information when a country is clicked
@app.callback(
    Output('selected_countries', 'children'),
    [Input('world-map', 'clickData')]
)
def display_click_data(clickData):
    print("Click data:", clickData)
    selected_countries = [point['location'] for point in clickData['points']]
    print("Selected countries", selected_countries)
    if len(selected_countries) == 2:
        return f'Selected countries : {selected_countries[0]} and {selected_countries[1]}'
    else:
        return "Ma porcoddio"

if __name__ == '__main__':
    app.run_server(debug = True)