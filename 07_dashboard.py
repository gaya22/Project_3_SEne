"""
File: 07_dashboard.py
Description: webpage runner that shows the study of the data.
"""

# Import the main libraries
import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_daq as daq
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly.io as pio
import dash_bootstrap_components as dbc
import auxiliary_functions as af
import statsmodels.api as sm

# Load and prepare dataframes
orig_df = pd.read_csv("GTF_export_cleaned.csv") # Upload the dataframe cleaned
orig_df["Month"] = pd.to_datetime(orig_df["Month"], format="mixed") # Re-setting the month as datetime object
orig_df = orig_df.set_index("Month", drop=True) # Re-setting the month as index
date_range = orig_df.index.values # Array of all the dates
tot_flows = af.countries_tot_flows(orig_df) # Dataframe with all af the countries (as index) and the total exit/enter flows of the whole period
exit_flow_countries = af.get_exit_countries(orig_df) # List of all the countries involved in the study that have extit flows
enter_flow_countries = af.get_enter_countries(orig_df) # list of all the countries involved in the study that have entry flows
feat_df = pd.read_csv("CleanData.csv") # Dataframe of possible features collected
feat_df.loc[:,'date'] = pd.to_datetime(feat_df.loc[:,'date'][:-1]) #Reinstating the index 
feat_df.set_index(['country','date'], inplace=True)
dfIT = pd.read_csv('Data_03.csv') # Dataframe of Italy data
dfIT["date"] = pd.to_datetime(dfIT["date"], format="mixed") # Re-setting the date as datetime object
dfIT = dfIT.set_index("date", drop=True) # Re-setting the month as index

# Creating the dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Creating the layout of the dashboard
app.layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.H1('Natural gas movements analysis'), # Title of the webpage
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
                        dcc.Store(id='selected-country-store', data=["Italy"]),
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
                            dcc.RadioItems(id='radio-direction',
                                options=[
                                    {'label': 'Outgoing', 'value': 'outgoing'},
                                    {'label': 'Incoming', 'value': 'incoming'},
                                    {'label': 'Net flow', 'value': 'net'}],
                                value = 'outgoing', inline=False),
                            html.Br(),
                        ], style={'width': '40%', 'float': 'right'})
                    ], style={'width': '55%', 'float': 'left'}),
                    html.Div(children=[ # Second column (right part) that hosts the graph
                        dcc.Graph(id="autocorrelation_graph"),
                        dcc.RadioItems(id='radio-simple-partial', # To change the graph
                                       options=[
                                           {'label': 'Simple Autocorrelation', 'value': 'simple'},
                                           {'label': 'Partial Autocorrelation', 'value': 'partial'}
                                       ], value = 'simple', inline = True)
                    ], style={'width': '45%', 'float': 'right'})
                ])
            ])
        ]),

        dcc.Tab(label='Features analysis', children=[ # Third tab - Exploring features
            html.Div(children=[
                html.H2("Features analysis"), # Title of the page
                html.P('This page shows data collected, that can be correlated to the gas movements'),html.Br(),
                html.Div(children=[
                    html.Div(children=[ # Left part of the page
                        html.P('Select the country'),
                        dcc.Dropdown(id='dropdown-country-2', options=af.get_country_feat_names(), multi=True),html.Br(),
                        html.P('Select the topic'),
                        dcc.Checklist(id='dropdown-topic', options=feat_df.columns.to_list()), html.Br()
                    ], style={'width': '18%', 'float': 'left'}),
                    html.Div(children=[ # Right part of the page
                        dcc.Graph(id='features-graph', style={'height':575})
                    ], style={'width': '82%', 'float': 'right'})
                ], style={'width':'100%', 'margin-bottom':'500px'}), html.Br(),
                html.Div([ # Last part in the bottom
                    html.P('It can be seen that the countries which have more dependency on gas are: Moldova, Malta, Netherlands, Latvia, Ireland, Lithuania and Italy.'),
                    html.P('The following table shows the maximum values registered of fraction of electricity generated by gas, of the mentioned countries.'),
                    html.P('It shows the relative month of registration and the GWh generated.'), html.Br(),
                    dash_table.DataTable(data=af.get_pick_gas(feat_df).to_dict('records'))
                ], style={'width':'90%', 'margin-top':'100px', 'float':'center'})

            ])
        ]),

        dcc.Tab(label='Italy data exploration', children=[ # Fourth tab - Italy data exploration
            html.Div([
                html.H2("Focus on Italy - exploring features"),
                html.P('Italy registered 12.8 GWh of electricity generated by natural gas during December 2022, that is the pick of Natural Gas usage for the electricity mix (57%).'),
                html.P('Considering this fact and the data availability of this country, the analysis will be focused on Italy.'),
                html.Div(children=[
                    html.Div(children=[ # Left part of the webpage containing the text
                        html.P('After a careful study of the data selected because they were hypothesized to be related to natural gas movements, the following considerations were drawn:'),
                        html.P(af.considerations()) # The big portion of text has been separated to facilitate the reading of the code
                    ], style={'width':'40%', 'float':'left', 'margin-top':'50px'}),
                    html.Div(children=[ # Right part of the webpage containing the graph
                        html.P('Below are shown relevant data of Italy, merged with the movements of natural gas. Here correlations can be studied. '),
                        dcc.Checklist(id='check-ita-data',
                                       options=dfIT.columns,
                                       inline=True),
                        dcc.Graph(id='italy-features-graph'),
                        daq.BooleanSwitch(id='normal-switch',on=True, label='Normalize (ON)', labelPosition='top'),
                    ], style={'width':'55%', 'float':'right', 'margin-top':'50px'})
                ])
                
            ])
        ]),

        dcc.Tab(label='Russo-Ukrainian War impact on Italy data', children=[ # Fifth tab - Russo-Ukrainian War
            html.Div([
                html.H2("Russo-Ukrainian war impact on Italian Gas movements"),
                html.P('As all of us might expect, the Russian-Ukrainin conflict coused a change in the trend of natural gas movement data.'),
                html.P('The aim of this section is to show how data changed, compared to how they would have been without this event. '),
                html.P(af.forecast_introduction())
            ])
        ])

    ])
])

#1 Callback to update the selected country in the store
@app.callback(
    Output('selected-country-store', 'data'),
    [Input('world-map', 'clickData')],
    [State('selected-country-store', 'data')]
)
def update_selected_country(clickData, current_country):
    if clickData and 'points' in clickData and clickData['points']:
        return clickData['points'][0]['location']
    return current_country

#1 App to be able to click in the map
@app.callback(
    Output('world-map', 'figure'),
    [Input('selected-country-store', 'data')]
)
def update_map(selected_country):
    if selected_country is not None:
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
                selectedpoints = [selected_country]
            )],
            'layout': go.Layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                )
            )
        }
    else:
        return {
            'data': [],
            'layout': {}
        }

#1 Callback to update the string above the graph
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

#1 Callback to update checklist options based on selected country and the direction
@app.callback(
    [Output('checklist-country-1', 'options'),
     Output('checklist-country-1', 'value')],
    [Input('world-map', 'clickData'),
     Input('radio-from-to', 'value')]
)
def update_checklist_options(clickData, direction):
    if clickData is not None and 'points' in clickData and clickData['points']: # If the map is clicked
        selected_country = clickData['points'][0]['location'] # selected_country defined
        flow_df = af.flows_from_direction(selected_country, orig_df, direction) # function defined in auxiliary functions
        country_names = flow_df.columns.values # Extract country names from column names
        options = [{'label': country, 'value': country} for country in country_names]
        return options, []
    else:
        return [], [] # Return empty options if no country is selected

#1 Callback to update graph based on selected country, checklist options and date range
@app.callback(
    Output('selected_country_graph', 'figure'),
    [Input('world-map', 'clickData'),
     Input('checklist-country-1', 'value'),
     Input('radio-from-to', 'value'),
     Input('date-range-slider', 'value')]
)
def update_country_graph(clickData, checked_countries, direction, valuerange):
    if clickData is not None and 'points' in clickData and clickData['points']:
        selected_country = clickData['points'][0]['location']
        flow_df = af.flows_from_direction(selected_country, orig_df, direction) # function defined in auxiliary functions
        if not flow_df.empty:
            start_date = flow_df.index.values[valuerange[0]]
            end_date = flow_df.index.values[valuerange[1]]
            flow_df = flow_df[start_date:end_date]
            data = []
            selected_columns = [item for item in checked_countries or []] # List created from "checked_countries"
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
            return {'data': [], 'layout': {}}
    else:
        return { # Return a default empty graph if no country is selected
            'data': [],
            'layout': {} 
        }

#1 Callback to update the paragraph that shows the timerange chosen
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

#1 Callback to save the figure and use the fade
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

#2 Callback to update the outgoing and incoming flows of the country in the autocorrelation tab 
@app.callback(
    [Output("outgoing-list", "children"),
     Output("incoming-list", "children")],
    Input("dropdown-countries", "value")
)
def update_relations_outgoing(country):
    flow_df_out = af.exit_flows(country, orig_df)
    flow_df_in = af.entry_flows(country, orig_df)
    country_list_out = af.list_of_columnnames(flow_df_out) # function that returns Ul list
    country_list_in = af.list_of_columnnames(flow_df_in) # function that returns Ul list
    par_out = f'Natural gas flows from {country}:'
    par_in = f'Natural gas flows to {country}:'
    return html.Div([par_out, country_list_out]), html.Div([par_in, country_list_in])

#2 Callback to manage the radio item for the countries in the autocorrelation tab
@app.callback(
        [Output('radio-countries', 'options'),
         Output('radio-countries', 'style'),
         Output('radio-countries', 'value')],
        [Input('dropdown-countries', 'value'),
         Input('radio-spec-tot', 'value'),
         Input('radio-direction', 'value')]
)
def update_radio_countries(country, type, direction):
    options = []
    if type == "specific":
        flow_df = af.flows_from_direction(country, orig_df, direction)
        country_names = flow_df.columns.values
        options = [{'label': country, 'value': country} for country in country_names]
        return options, {'display': 'block'}, None
    else:
        return options, {'display': 'none'}, None

#2 Callback to update the autocorrelation graph
@app.callback(
    Output('autocorrelation_graph', 'figure'),
    [Input('dropdown-countries', 'value'),
     Input('radio-spec-tot', 'value'),
     Input('radio-direction', 'value'),
     Input('radio-countries', 'value'),
     Input('radio-simple-partial', 'value')]
)
def update_autocorrelation_graph(country_1, type, direction, country_2, corr):
    if None in [country_1, type, direction, country_2, corr]:
        return {}  # Return an empty figure if any input is None
    flow_df = af.flows_from_direction(country_1, orig_df, direction) # Getting the dataframe specific of the selected conutry_1 and the direction
    flows = pd.DataFrame() # Create a empty df that will be used for graph
    if type == "specific":
        if country_2 != None: # Country_2 is selected
            flows[country_2] = flow_df[country_2] # Getting just the column of specific country_2
            my_str = f' - {country_2}' # For the title of the graph
        else: # Country_2 is not selected yet
            return {}
    elif type == "tot":
        flows["total"] = flow_df.sum(axis=1) # Sum each row
        my_str = "" # For the title of the graph
    lab = f'of {direction} flow of {country_1} {my_str}' # Creating reference for title
    if corr == "simple":
        flows['lagged'] = flows.iloc[:,0].shift(1) # Creating the second column of lagged value
        flows.dropna(inplace=True)
        figure = px.scatter(x=flows.iloc[:,0].values, y=flows['lagged'].values) # Creating graph
        figure.update_layout(xaxis_title="Current Values", yaxis_title="Lagged Values (+1)",
                            title=f'Simple Autocorrelation {lab}') # Putting the title and the labels
    else: # Partial correlation is selected
        pacf = sm.tsa.stattools.pacf(flows.iloc[:,0])
        figure = px.line(x=list(range(len(pacf))), y=pacf,
                         title=f'Partial Autocorrelation {lab}',
                         labels={'x':'Lag', 'y':'Partial Autocorrelation'})
    return figure

#3 Callback to update the feature analysis graph
@app.callback(
    Output('features-graph', 'figure'),
    [Input('dropdown-country-2', 'value'),
     Input('dropdown-topic', 'value')]
)
def update_features_graph(countries, topics):
    df1 = pd.DataFrame(index=feat_df.index.get_level_values('date').unique().tolist())
    if countries is not None and topics is not None:
        for countr in countries:
            cod = next(key for key, value in af.country_mapping.items() if value == countr)
            for top in topics:
                colname = countr + " - " + top
                result = feat_df.loc[(cod, slice(None)), top]
                result.index = result.index.droplevel('country')
                df1[colname] = result
        data = []
        for col in df1:
            trace = go.Scatter(x=df1.index, y=df1[col], mode='lines',
                               name=col, showlegend=True)
            data.append(trace)
        layout=go.Layout(
            title='Features exploring',
            xaxis=dict(title='Month'),
            legend = dict(y=1.02, yanchor='top', x=0),
            height=600
        )
        figure = go.Figure(data=data, layout=layout)
    else: figure = {'data':[], 'layout': {}}
    return figure

#4 Callback to update the graph of Italy features
@app.callback(
    Output('italy-features-graph', 'figure'),
    [Input('check-ita-data', 'value'),
     Input('normal-switch', 'on')]
)
def features_italy_graph(topic, on):
    data = []
    layout = {}
    if topic is not None:
        dfIT1 = dfIT[topic]
        if on:
            for column in dfIT1.columns:
                dfIT1.loc[:,column] = (dfIT1.loc[:,column] - dfIT1.loc[:,column].min())/(dfIT1.loc[:,column].max() - dfIT1.loc[:,column].min())
        for col in dfIT1:
            trace = go.Scatter(x=dfIT1.index, y=dfIT1[col], mode='lines',
                               name=col, showlegend=True)
            data.append(trace)
        layout = go.Layout(
            xaxis=dict(title='Month'),
            legend= dict(y=1.02, yanchor='top', x=0),
            height=600
        )
    figure = go.Figure(data=data, layout=layout)
    
    return figure

if __name__ == '__main__':
    app.run_server(debug = True)