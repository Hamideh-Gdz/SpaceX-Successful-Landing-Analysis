# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"E:\DATA SCIENCE\COURSERA\Course10/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                                                        [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 
                                    2500: '2500', 
                                    5000: '5000', 
                                    7500: '7500', 
                                    10000: '10000'},
                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        success_count = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(success_count, values='class', 
        names='Launch Site', 
        labels={'Launch Site': 'Launch Site', 'class': 'Total successful launches'},
        title="Total successful launches for each site")
        return fig
    else:
        # return the outcomes piechart for a selected site
        # Filter data for the selected launch site
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]

        # Count the occurrences of Class 1 (Success) and Class 0 (Failure)
        class_counts = filtered_df["class"].value_counts().reset_index()
        class_counts.columns = ["class", "Count"]  # Rename columns

        # Define labels for the pie chart
        class_counts["class"] = class_counts["class"].replace({1: "Success", 0: "Failure"})

        # Create a pie chart
        fig = px.pie(class_counts, names="class", values="Count", title=f"Launch Success vs Failure at {entered_site}")
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= payload_range[0]) & 
                            (spacex_df["Payload Mass (kg)"] <= payload_range[1])]
    if entered_site == 'ALL':
        # success_count = spacex_df.groupby("Launch Site")["class"].sum()
        fig = px.scatter(filtered_df,  
                            x="Payload Mass (kg)",          
                            y="class",                
                            color="Booster Version Category",   # Color by booster version
                            # size="PayloadMass",       # Adjust marker size by payload mass
                            # hover_data=["LaunchSite"],# Additional info on hover
                            title=f"Payload Mass vs. Launch Outcome (Payload Range: {payload_range[0]} - {payload_range[1]} kg)")
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_data = spacex_df[(spacex_df["Launch Site"] == entered_site) &
                                (spacex_df["Payload Mass (kg)"] >= payload_range[0]) & 
                                (spacex_df["Payload Mass (kg)"] <= payload_range[1])]
        fig = px.scatter(site_data,  
                            x="Payload Mass (kg)",          
                            y="class",                
                            color="Booster Version Category",   # Color by booster version
                            # size="PayloadMass",       # Adjust marker size by payload mass
                            # hover_data=["LaunchSite"],# Additional info on hover
                            title=f"Payload Mass vs. Launch Outcome for {entered_site} (Payload Range: {payload_range[0]} - {payload_range[1]} kg)")
        return fig
# Run the app
if __name__ == '__main__':
    app.run()
