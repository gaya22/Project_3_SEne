"""
File: 07_dashboard.py
Description: webpage runner that shows the study of the data.
"""

# Import the main libraries
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os
import numpy as np
import auxiliary_functions as af

# Load and prepare dataframes
orig_df = pd.read_csv("GTF_export_cleaned.csv") # Upload the dataframe cleaned
orig_df["Month"] = pd.to_datetime(orig_df["Month"], format="mixed") # Re-setting the month as datetime object
orig_df = orig_df.set_index("Month", drop=True) # Re-setting the month as index
date_range = orig_df.index.values # Array of all the dates
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
                    html.Div(children=[ # Left part of the webpage
                        html.P("Select a country to plot the outgoing or incoming natural gas flows"),
                        dcc.RadioItems(id="radio-from-to",
                                    options=[
                                        {'label': 'Outgoing', 'value': 'from'},
                                        {'label': 'Incoming', 'value': 'to'}],
                                    value = 'from',
                                    inline=True),
                        dcc.Graph(id="world-map",
                                  config={'scrollZoom': True},
                                  clickData={'points': []},
                                  style={'width':'100%', 'height':'65vh'}),
                    ], style={'width': '45%', 'float': 'left'}),
                    html.Div(children=[ # Right part of the webpage
                        html.P(id="checklist-paragraph"), # there is a callback that updates the paragraph (update_paragraph)
                        dcc.Checklist(id = "checklist-country",
                                      # options = there is a callback that updates it (update_checklist_options)
                                      inline=True),
                        dcc.Graph(id='selected_country_graph'), # Graph of values
                        dcc.RangeSlider(id='date-range-slider',
                                        marks = None,
                                        min=0,
                                        max=len(date_range)-1,
                                        step=1,
                                        value=[0, len(date_range)-1], # Initial date range
                                        ),
                        html.Div([
                            html.Button("Download figure", id="btn-download"),
                            dcc.Download(id="download"),
                            html.A("Download", id="download-link", download="figure.png", href="", target="_blank", style={'display':'none'})
                        ])
                    ], style={'width': '55%', 'float': 'right'})
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
    selected_country = [point['location'] for point in clickData['points']]
    return {
        'data': [go.Choropleth(
            locations=tot_flows.index,
            z=tot_flows["tot_exit_flows"], # The color of the map is based on the exit flows
            locationmode='country names',
            text=tot_flows.index,
            colorscale='Viridis',
            autocolorscale=False,
            marker_line_color='black',
            marker_line_width=0.5,
            hoverinfo='text',
            selectedpoints = selected_country
        )],
        'layout': go.Layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
    }

# Callback to update the string above the graph
@app.callback(
        Output('checklist-paragraph', 'children'),
        Input('radio-from-to', 'value')
)
def update_paragraph(direction):
    if direction == "from":
        prep = 'to'
    else:
        prep = 'from'
    return 'Select countries '+ prep + ' which natural gas flows'

# Callback to update checklist options based on selected country
@app.callback(
    Output('checklist-country', 'options'),
    [Input('world-map', 'clickData'),
     Input('radio-from-to', 'value')]
)
def update_checklist_options(clickData, direction):
    if clickData and 'points' in clickData and clickData['points']: # If the map is clicked
        selected_country = clickData['points'][0]['location'] # selected_country defined
        if direction == "from":
            flow_df = af.exit_flows(selected_country, orig_df) # dataframe of the exit flows
        else:
            flow_df = af.entry_flows(selected_country, orig_df) # dataframe of the entry flows
        country_names = flow_df.columns.values # Extract country names from column names
        options = [{'label': country, 'value': country} for country in country_names]
        return options
    else:
        return [] # Return empty options if no country is selected

# Callback to update graph based on selected country, checklist options and date range
@app.callback(
    Output('selected_country_graph', 'figure'),
    [Input('world-map', 'clickData'),
     Input('checklist-country', 'value'),
     Input('radio-from-to', 'value'),
     Input('date-range-slider', 'value')]
)
def update_country_graph(clickData, checked_countries, direction, valuerange):
    if clickData and 'points' in clickData and clickData['points']:
        selected_country = clickData['points'][0]['location']
        if direction == "from":
            flow_df = af.exit_flows(selected_country, orig_df) # dataframe of the exit flows
            prep = "from "
        else:
            flow_df = af.entry_flows(selected_country, orig_df) # dataframe of the entry flows
            prep = "to "
        start_date = flow_df.index.values[valuerange[0]]
        end_date = flow_df.index.values[valuerange[1]]
        flow_df = flow_df[start_date:end_date]
        data = []
        selected_columns = [item for item in checked_countries or []] # List created from "checked_countries" that is the same as the index of "exits"
        for col in selected_columns:
            trace = go.Scatter(
                x=flow_df.index,
                y=flow_df[col],
                mode='lines',
                name=col,
                showlegend= True
            )
            data.append(trace)
        layout = go.Layout(
            title= f'Natural gas movements {prep, selected_country}',
            xaxis=dict(title='Month'),
            yaxis=dict(title='m³')
        )
        figure = go.Figure(data=data, layout=layout)
        return figure
    else:
        # Return a default empty graph if no country is selected
        return {
            'data': [],
            'layout': {}
        }
    
# Callback to download figures
@app.callback(
    Output("download", "data"),
    [Input("btn-download", "n_clicks"),
     Input("selected_country_graph", "figure")],
    prevent_initial_call = True
)
def download_fig(n_clicks, figure):
    if n_clicks is not None and figure:
        pio.write_image(figure, "figure.png")
        file_path = os.path.abspath("figure.png")
        return dict(content=file_path, filename="figure.png")
    else:
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug = True)