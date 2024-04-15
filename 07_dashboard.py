"""
File: 07_dashboard.py
Description: webpage runner that shows the study of the data.
"""

# Import the main libraries
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import dash_bootstrap_components as dbc
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
                    ], style={'width': '43%', 'float': 'left'}),
                    html.Div(children=[ # Right part of the webpage
                        html.P(id="checklist-paragraph"), # there is a callback that updates the paragraph (update_checklist_paragraph)
                        dcc.Checklist(id = "checklist-country-1", # There is a callback that updates it (update_checklist_options)
                                      inline=True),
                        dcc.Graph(id='selected_country_graph'), # Graph of values 
                        html.P(id="time-range-parag"), # there is a callback that updates the paragraph (update_timerange_paragraph)
                        html.P('Use the slider to modify the period'),
                        dcc.RangeSlider(id='date-range-slider', marks = None,
                                        min=0, max=len(date_range)-1,
                                        step=1, value=[0, len(date_range)-1], # Initial date range
                                        ),
                        html.Div([
                            dbc.Button("Save figure", id="btn-save", className="mb-3", n_clicks=0), # Button to save figure
                            dbc.Fade(  # Save figure button
                                dbc.Card(dbc.CardBody(
                                        html.P("The figure has been saved in the work directory as \"figure.png\"", className="card-text"))
                                ), id="fade", is_in=False, appear=False), 
                        ])
                    ], style={'width': '53%', 'float': 'right'})
                ])
            ])
        ]),

        dcc.Tab(label='Natural gas autocorrelation', children=[ # Second tab - Autocorrelation
            html.Div([
                html.H2("Natural gas autocorrelation"),
                html.Div(children=[ # Divide the webpage in 2 columns
                    html.Div(children=[ # First column (left part) that will be divided in 2 columns
                        html.Div(children=[ # Left part of the webpage
                            html.P('Select a country to study its flows of natural gas'),
                            dcc.Dropdown(tot_flows.index.sort_values(), "Italy", id="dropdown-countries"),
                            html.Div(children=[ # Divide the space into 2 columns for outgoing and incoming
                                html.Div(html.P(id="outgoing-list"),  # The function update_relations_outgoing updates the list
                                         style={'width': '50%', 'float': 'left'}),
                                html.Div(html.P(id="incoming-list"), style={'width': '50%', 'float': 'right'}) # The function update_relations_incoming updates the list
                            ])
                        ], style={'width': '55%', 'float': 'left'}),
                        html.Div(children=[ # Center part of the webpage
                            # Here I put the options for the plot
                            html.P('Select the option to study a specific relation or the total flow'),
                            dcc.RadioItems(id="radio-spec-tot",
                                    options=[
                                        {'label': 'Flow related to a specific country', 'value': 'specific'},
                                        {'label': 'Total flow', 'value': 'tot'}],
                                    value = 'specific', inline=False),
                            html.Br(),
                            dcc.RadioItems(id = "radio-countries", inline=True, style={'display':'none'}), # There is a callback that updates the options
                            html.Br(),
                            html.P('Select the direction'),
                            dcc.RadioItems(id="radio-direction",
                                options=[
                                    {'label': 'Outgoing', 'value': 'from'},
                                    {'label': 'Incoming', 'value': 'to'},
                                    {'label': 'Net flow', 'value': 'net'}],
                                value = 'out', inline=False),
                            html.Br(),
                        ], style={'width': '40%', 'float': 'right'})
                    ], style={'width': '55%', 'float': 'left'}),
                    html.Div(children=[ # Second column (right part) that hosts the graph
                        dcc.Graph(id="autocorrelation_graph")
                    ], style={'width': '45%', 'float': 'right'})
                ])
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
def update_checklist_paragraph(direction):
    if direction == "from":
        prep = 'to'
    else:
        prep = 'from'
    return 'Select countries '+ prep + ' which natural gas flows'

# Callback to update checklist options based on selected country
@app.callback(
    Output('checklist-country-1', 'options'),
    [Input('world-map', 'clickData'),
     Input('radio-from-to', 'value')]
)
def update_checklist_options(clickData, direction):
    if clickData and 'points' in clickData and clickData['points']: # If the map is clicked
        selected_country = clickData['points'][0]['location'] # selected_country defined
        flow_df = af.flows_from_direction(selected_country, orig_df, direction) # function defined in auxiliary functions
        country_names = flow_df.columns.values # Extract country names from column names
        options = [{'label': country, 'value': country} for country in country_names]
        return options
    else:
        return [] # Return empty options if no country is selected

# Callback to update graph based on selected country, checklist options and date range
@app.callback(
    Output('selected_country_graph', 'figure'),
    [Input('world-map', 'clickData'),
     Input('checklist-country-1', 'value'),
     Input('radio-from-to', 'value'),
     Input('date-range-slider', 'value')]
)
def update_country_graph(clickData, checked_countries, direction, valuerange):
    if clickData and 'points' in clickData and clickData['points']:
        selected_country = clickData['points'][0]['location']
        flow_df = af.flows_from_direction(selected_country, orig_df, direction) # function defined in auxiliary functions
        start_date = flow_df.index.values[valuerange[0]]
        end_date = flow_df.index.values[valuerange[1]]
        flow_df = flow_df[start_date:end_date]
        data = []
        selected_columns = [item for item in checked_countries or []] # List created from "checked_countries" that is the same as the index of "exits"
        for col in selected_columns: # Creating the graph
            trace = go.Scatter(x=flow_df.index, y=flow_df[col], mode='lines',
                name=col, showlegend= True)
            data.append(trace)
        layout = go.Layout( # Defining the layout of the graph
            title= f'Natural gas movements {direction} {selected_country}',
            xaxis=dict(title='Month'),
            yaxis=dict(title='m³')
        )
        figure = go.Figure(data=data, layout=layout)
        return figure
    else:
        return { # Return a default empty graph if no country is selected
            'data': [],
            'layout': {} 
        }

# Callback to update the paragraph that shows the timerange chosen
@app.callback(
    Output("time-range-parag", "children"),
    Input('date-range-slider', 'value')
)
def update_timerange_paragraph(valuerange):
    start_date = orig_df.index.values[valuerange[0]]
    end_date = orig_df.index.values[valuerange[1]]
    start = af.get_month(start_date)
    end = af.get_month(end_date)
    return f'Monthly data shown from {start} to {end}.'

# Callback to save the figure and use the fade
@app.callback(
    Output("fade", "is_in"),
    [Input("btn-save", "n_clicks"),
     Input("selected_country_graph", "figure")],
    [State('fade', 'is_in')]
)
def toggle_modal(n, figure, is_in):
    if not n:
            return False
    else:
        if figure is not None:
            pio.write_image(figure, "figure.png")
        return not is_in

# Callback to update the outgoing flows of the country in the autocorrelation tab 
@app.callback(
    Output("outgoing-list", "children"),
    Input("dropdown-countries", "value")
)
def update_relations_outgoing(country):
    flow_df = af.exit_flows(country, orig_df)
    country_names = flow_df.columns.values # Extract country names from column names
    country_list_items = [html.Li(country_name) for country_name in country_names]
    country_list = html.Ul(country_list_items)
    paragraph = f'Natural gas flows from {country}:'
    return html.Div([paragraph, country_list])

# Callback to update the incoming flows of the country in the autocorrelation tab
@app.callback(
    Output("incoming-list", "children"),
    Input("dropdown-countries", "value")
)
def update_relations_incoming(country):
    flow_df = af.entry_flows(country, orig_df)
    country_names = flow_df.columns.values # Extract country names from column names
    country_list_items = [html.Li(country_name) for country_name in country_names]
    country_list = html.Ul(country_list_items)
    paragraph = f'Natural gas flows to {country}:'
    return html.Div([paragraph, country_list])

# Callback to manage the radio item for the countries in the autocorrelation tab
@app.callback(
        [Output('radio-countries', 'options'),
         Output('radio-countries', 'style')],
        [Input('dropdown-countries', 'value'),
         Input('radio-spec-tot', 'value'),
         Input('radio-direction', 'value')]
)
def update_radio_countries(country, type, direction):
    options = []
    if type == "specific" and direction != "net":
        flow_df = af.flows_from_direction(country, orig_df, direction)
        country_names = flow_df.columns.values
        options = [{'label': country, 'value': country} for country in country_names]
        return options, {'display': 'block'}
    else:
        return options, {'display': 'none'}

# Callback to update the autocorrelation graph
@app.callback(
    Output('autocorrelation_graph', 'figure'),
    [Input('dropdown-countries', 'value'),
     Input('radio-spec-tot', 'value'),
     Input('radio-direction', 'value')]
)
def update_autocorrelation_graph(country, type, direction):
    return None


if __name__ == '__main__':
    app.run_server(debug = True)