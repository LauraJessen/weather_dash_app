# Importing the libraries
import pandas as pd
import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc

# reading the data and preparing it for the tables and graphs
df = pd.read_csv("weekly_avg.csv")
df = df.sort_values(by="week_num")

# creating the table
df_week1 = df[df['week_num'] == 1].drop(columns=['lat','lon'])
table = dash_table.DataTable(df_week1.to_dict('records'),
                            [{'name': i, 'id': i} for i in df_week1.columns],
                            style_data={'color': 'white', 'backgroundColor': 'green', 'font-family': 'Helvetica'},
                            #update: header
                            style_header={'text':'black', 'backgroundColor': 'green', 'font-family': 'Helvetica'})



#creating the line graph
df_line = px.line(df, x='week_num', y='avg_temp', color='city', height=400, width= 900, range_x=[1,52], range_y=[-20,30])

df_line = dcc.Graph(figure=df_line)

#creating the map
map = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     color='avg_temp',
                     #changing markers size
                     size='avg_temp',
                     size_max=40,
                     text='city',
                     projection='natural earth',
                     title='11 cities',
                     color_continuous_scale=px.colors.sequential.Plasma,
                     #update range to fix values 
                     range_color= (-20, 30),
                     #update: added animation_frame and height 
                     animation_frame= 'week_num',
                     height= 600)
map = dcc.Graph(figure=map)

#creating dropdown
dropdown = dcc.Dropdown(['Irkutsk',
 'Krakau',
 'Saskatoon',
 'Bremen',
 'London',
 'Dublin',
 'Amsterdam',
 'Minsk',
 'Berlin',
 'Birmingham',
'Rio Gallegos'], ['Berlin'], multi=True, style ={'font-family': 'Helvetica', "color": "black"})



############## using the app with radio item
app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server



app.layout = html.Div([html.H1('CWL', style={'textAlign': 'center', 'color': 'green', 'font-family': 'Helvetica', 'font-size': '24px'}), 
                      
                       html.H2('Cities with Latitude', style ={'paddingLeft': '30px', 'textAlign': 'center', 'color': 'green', 'font-family': 'Helvetica', 'font-size': '24px'}),
                       html.H3('11 cities at around 52 degrees latitude', style ={'paddingLeft': '30px', 'textAlign': 'center', 'color': 'green', 'font-family': 'Helvetica'}),
                       html.Div([html.Div('All the cities', style ={'font-family': 'Helvetica'}), dropdown, df_line, table, map])

                    
])

@callback(
    Output(df_line, "figure"), 
    Input(dropdown, "value"))

def update_line_chart(selected_cities): 
    mask = df["city"].isin(selected_cities)
    if not selected_cities:
        fig =px.bar(df[mask], x='week_num', y='avg_temp', color='city', height=400, width= 700, 
            range_x=[1,52], range_y=[-20,30], title = "all cities")
    else: 
        fig = px.line(df[df['city'].isin(selected_cities)], x='week_num', y='avg_temp', color='city', title='Selected Cities')

        
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="yellow")
  
    return fig

if __name__ == '__main__':
     app.run_server()
