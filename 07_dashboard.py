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
orig_df = pd.read_csv("GTF_export_cleaned.csv") # Upload the dataframe cleaned
orig_df["Month"] = pd.to_datetime(orig_df["Month"], format="mixed") # Re-setting the month as datetime object
orig_df = orig_df.set_index("Month", drop=True) # Re-setting the month as index
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
                        html.P("Select a country to plot the outgoing and incoming natural gas flows"),
                        dcc.RadioItems(id="radio-from-to",
                            options=[
                                {'label': 'From', 'value': 'from'},
                                {'label': 'To', 'value': 'to'}],
                            value = 'from',
                            inline=True),
                        dcc.Graph(id="world-map",
                                  config={'scrollZoom': True},
                                  clickData={'points': []},
                                  style={'width':'100%', 'height':'80vh'}),
                    ], style={'width': '45%', 'float': 'left'}),
                    html.Div(children=[ # Right part of the webpage
                        dcc.Checklist(id = "checklist-country",
                                      # options = update options based on the selected country on map
                                      ),
                        dcc.Graph(id='selected_country_graph')
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
    selected_countries = [point['location'] for point in clickData['points']]
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
            selectedpoints = selected_countries
        )],
        'layout': go.Layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
    }

# Callback to update checklist options based on selected country
@app.callback(
    Output('checklist-country', 'options'),
    [Input('world-map', 'clickData')]
)
def update_checklist_options(clickData):
    if clickData and 'points' in clickData and clickData['points']:
        selected_country = clickData['points'][0]['location']
        exits = af.exit_flows(selected_country, orig_df)
        # Extract country names from column names
        country_names = [col.split('to')[1] for col in exits.columns]
        options = [{'label': country, 'value': country} for country in country_names]
        return options
    else:
        # Return empty options if no country is selected
        return []

# Callback to update graph based on selected country and checklist options
@app.callback(
    Output('selected_country_graph', 'figure'),
    [Input('world-map', 'clickData'),
     Input('checklist-country', 'value')]
)
def update_country_graph(clickData, selected_countries):
    if clickData and 'points' in clickData and clickData['points']:
        selected_country = clickData['points'][0]['location']
        exits = af.exit_flows(selected_country, orig_df)
        data = []
        # Filter columns based on selected countries in the checklist
        selected_columns = ['to' + country for country in selected_countries]
        for col in selected_columns:
            trace = go.Scatter(
                x=exits.index,
                y=exits[col],
                mode='lines',
                name=col
            )
            data.append(trace)
        layout = go.Layout(
            title='Line Plot Over Time',
            xaxis=dict(title='Month'),
            yaxis=dict(title='Value')
        )
        figure = go.Figure(data=data, layout=layout)
        return figure
    else:
        # Return a default empty graph if no country is selected
        return {
            'data': [],
            'layout': {}
        }

if __name__ == '__main__':
    app.run_server(debug = True)