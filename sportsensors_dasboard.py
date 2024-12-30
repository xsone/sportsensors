import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
#import mysql.connector
import pandas as pd
import plotly.express as px
from pygments.lexers import go
import datetime
import os
# import matplotlib.pyplot as plt
# import csv

#Query om verschil kolom aan te brengen
#UPDATE energiemeter JOIN (SELECT id, waterLtr - LAG(waterLtr, 1) OVER (ORDER BY id) AS waterACTgebruik FROM energiemeter) AS subquery ON energiemeter.id = subquery.id SET energiemeter.waterACTgebruik = subquery.waterACTgebruik

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Initial data
vandaag = datetime.datetime.now()
gisteren = vandaag - datetime.timedelta(days=1)
morgen = vandaag + datetime.timedelta(days=1)
print('Gisteren: ', gisteren)
print('Vandaag: ', vandaag)
print('Morgen: ', morgen)

#start_date = "20241207"
start_date = vandaag.strftime("%Y%m%d")
#end_date = "20241207"
end_date = start_date

# Define the path to the CSV file
synology_path = "//DS218J/software/Sportdata/sportlog"
file_path = os.path.join(synology_path, "sportlog" + start_date + ".csv")

df = pd.read_csv(file_path, delimiter=';')
print(df.head())
print("Column names:", df.columns.tolist())

# Access the 'time' column if it exists
if 'time' in df.columns:
    time_column = df['time']
    print(time_column.head())
else:
    print("Column 'time' does not exist in the DataFrame.")

# Prepare data for two lines
df_long = pd.melt(df, id_vars=['time'], value_vars=['Ffront', 'Fback'], var_name='Type', value_name='Value')
fig1 = px.line(df_long, x='time', y='Value', color='Type', title='F-front and F-back',
                      labels={'Value': 'Electricity', 'datum': 'Date'},
                      color_discrete_map={ 'Ffront': 'blue', 'Fback': 'red' })
fig2 = px.line(df, x='time', y='Xas', title='Xas', color_discrete_sequence=['purple'])
fig3 = px.line(df, x='time', y='Fback', title='Fback', color_discrete_sequence=['red'])
fig4 = px.line(df, x='time', y='Yas', title='Yas', color_discrete_sequence=['orange'])

# Define the layout of the app
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col([
            html.H1("Sport Sensor Data, (c) Jack Cop"),
            dcc.DatePickerRange(
                id='date-picker-range',
                # start_date='2024-11-29',
                # end_date='2024-12-01',
                start_date=vandaag,
                end_date=start_date,
                display_format='YYYY-MM-DD'
            ),
            html.Button('Submit', id='submit-button', n_clicks=0),
            #dcc.Graph(id='example-graph', figure=fig)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='graph-1', figure=fig1)], width=6),
        dbc.Col([dcc.Graph(id='graph-2', figure=fig2)], width=6),
        dbc.Col([dcc.Graph(id='graph-3', figure=fig3)], width=6),
        dbc.Col([dcc.Graph(id='graph-4', figure=fig4)], width=6)
    ])
])

# Define the callback to update the graph based on the selected date range
@app.callback(
    #Output('example-graph', 'figure'),
    [Output('graph-1', 'figure'), Output('graph-2', 'figure'), Output('graph-3', 'figure'), Output('graph-4', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(n_clicks, start_date, end_date):
    #df = fetch_data(start_date, end_date)

    # Prepare data for two lines
    df_long = pd.melt(df, id_vars=['time'], value_vars=['Ffront', 'Fback'], var_name='Type', value_name='Value')
    fig1 = px.line(df_long, x='time', y='Value', color='Type', title='F-front and F-back',
                   labels={'Value': 'Electricity', 'datum': 'Date'},
                   color_discrete_map={'Ffront': 'blue', 'Fback': 'red'})
    fig2 = px.line(df, x='time', y='Xas', title='Xas', color_discrete_sequence=['purple'])
    fig3 = px.line(df, x='time', y='Fback', title='Fback', color_discrete_sequence=['red'])
    fig4 = px.line(df, x='time', y='Yas', title='Yas', color_discrete_sequence=['orange'])
    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True)
