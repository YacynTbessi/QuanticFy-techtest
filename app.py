import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import plotly.express as px

# Set your Mapbox access token here
mapbox_token = 'pk.eyJ1IjoieXZjeW4iLCJhIjoiY2xwaXNsNmV4MDJ3YjJqcG53OTBwcmFuNSJ9.RLuvzHJqNWgrTOljiQKFsw'

# SQLite database connection
conn = sqlite3.connect('test.db')

# Read data from the database into a Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM test", conn)

# Convert 'nbre_pdc' to numeric
df['nbre_pdc'] = pd.to_numeric(df['nbre_pdc'], errors='coerce')

# Convert 'puissance_nominale' to numeric
df['puissance_nominale'] = pd.to_numeric(df['puissance_nominale'], errors='coerce')

# Close the database connection
conn.close()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app with additional CSS styles and fonts
app.layout = html.Div([
    html.H1("Electric Vehicle Charging Stations in Paris", style={'font-family': 'Arial, sans-serif', 'color': '#333'}),

    # Dropdown for selecting the arrondissement
    dcc.Dropdown(
        id='arrondissement-dropdown',
        options=[{'label': arr, 'value': arr} for arr in df['arrondissement'].unique()],
        value=df['arrondissement'].unique()[0],
        multi=False,
        style={'width': '50%', 'margin-bottom': '20px'}
    ),

    # Plotly express scatter map
    dcc.Graph(id='charging-stations-map'),

    # Heatmap
    dcc.Graph(id='heatmap'),

    # Scatter plot
    dcc.Graph(id='scatter-plot'),
], style={'font-family': 'Arial, sans-serif', 'margin': '20px', 'background-color': '#f5f5f5'})

# Define callback to update the map and charts based on dropdown selection
@app.callback(
    [Output('charging-stations-map', 'figure'),
     Output('heatmap', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('arrondissement-dropdown', 'value')]
)
def update_graphs(selected_arr):
    # Update the map
    filtered_df = df[df['arrondissement'] == selected_arr]
    map_fig = px.scatter_mapbox(
        filtered_df,
        lat='coordonneesxy_lat',
        lon='coordonneesxy_lon',
        text='nom_station',
        hover_name='arrondissement',
        color='nbre_pdc',
        size='nbre_pdc',
        title=f"Charging Stations in {selected_arr}",
        mapbox_style="streets",  # Use 'streets' or 'outdoors' for the free Mapbox style
        zoom=12,
        center=dict(
            lat=filtered_df['coordonneesxy_lat'].mean(),
            lon=filtered_df['coordonneesxy_lon'].mean()
        ),
    )
    map_fig.update_layout(mapbox=dict(accesstoken=mapbox_token), autosize=True, hovermode='closest')

    # Heatmap
    heatmap_fig = px.density_heatmap(
        df,
        x='coordonneesxy_lon',
        y='coordonneesxy_lat',
        title='Charging Station Distribution Across Arrondissements',
        labels={'coordonneesxy_lon': 'Longitude', 'coordonneesxy_lat': 'Latitude'},
    )

    # Scatter plot
    scatter_plot_fig = px.scatter(
        df,
        x='puissance_nominale',
        y='nbre_pdc',
        size='nbre_pdc',
        color='arrondissement',
        title='Scatter Plot: Power vs. Number of Charging Points',
        labels={'puissance_nominale': 'Power(kW)', 'nbre_pdc': 'Number of Charging Points'}
    )

    return map_fig, heatmap_fig, scatter_plot_fig

# Run the app
if __name__ == '__main__':
     app.run_server(debug=True, host="0.0.0.0", port=8081, use_reloader=False)
