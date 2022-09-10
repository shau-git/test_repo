# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

sites = spacex_df['Launch Site'].unique()
default_option = 'ALL'
options = [{'label': 'All Sites', 'value': default_option}]
for site in sites:
    options.append({'label': site, 'value': site})

site_dropdown_id = 'site-dropdown'

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div([
                                    dcc.Dropdown(id = site_dropdown_id,
                                        options = options,
                                        value = default_option,
                                        placeholder = 'Select a Launch Site here',
                                        searchable = True)
                                ]),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0, 
                                                max=10000, 
                                                step=1000,
                                                marks={0: '0', 1000: '1000', 2000: '2000', 
                                                       3000: '3000', 4000: '4000', 5000: '5000', 
                                                       6000: '6000', 7000: '7000', 8000: '8000', 
                                                       9000: '9000', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id=site_dropdown_id, component_property='value'))
def get_pie_chart(selected_site):
    df = spacex_df[['Launch Site', 'class']]
    if selected_site == 'ALL':
        df_all = df.groupby('Launch Site').sum().reset_index()
        fig = px.pie(df_all, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        df_site = df[df['Launch Site'] == selected_site]
        df_site = df_site['class'].value_counts().rename_axis('class').to_frame('counts').reset_index()
        fig = px.pie(df_site, values='counts', names='class', title='Total Success Launches for site ' + selected_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id=site_dropdown_id, component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(selected_site, payload):
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
    if selected_site == 'ALL':
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        df = df[df['Launch Site'] == selected_site]
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
        

# Run the app
if __name__ == '__main__':
    app.run_server()
