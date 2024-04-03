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
exit_flow_countries = af.get_exit_countries(orig_df)
enter_flow_countries = af.get_enter_countries(orig_df)

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
                        dcc.Graph(id="world-map", config={'scrollZoom': False})
                    ], style={'width': '70%', 'display': 'inline-block'}),
                    html.Div(children=[ # Second column
                        html.Div(id='output_country'),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=datetime(2008, 10, 1),
                            max_date_allowed=datetime(2024, 1, 1),
                            initial_visible_month=datetime(2008, 10, 1),
                            start_date=datetime(2008, 10, 1),
                            end_date=datetime(2024, 1, 1)
                            )
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

# Callback to update information when a country is clicked
@app.callback(
    Output('output_country', 'children'),
    [Input('world-map', 'clickData')]
)
def display_click_data(clickData):
    country = "restart"
    if clickData:
        if country == "restart": # Means that the user is selecting the exit country
            country = clickData['points'][0]['location']
            if country in exit_flow_countries:
                    exit = country
            else:
                country = "restart"
                return f'This country has not exit flows. Please choose another one.'
        else: # The user is selecting the enter country
            country = clickData['points'][0]['location']
            if country in enter_flow_countries:
                enter = country
            else:
                return f'This country has not enter flows. Please restart.'
            country = "restart" # To restart from the exit country

    else:
        return 'Click on a country to see details.'

# App to be able to click in the map
@app.callback(
    Output('world-map', 'figure'),
    [Input('world-map', 'clickData')]
)
def update_map(clickData):
    # Update Choropleth trace based on selected countries and date range
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