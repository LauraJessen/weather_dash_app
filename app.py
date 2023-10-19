# Importing the libraries

import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc

# reading the data and preparing it for the tables and graphs
df = px.data.gapminder()
df_germany = df[df['country']=='Germany']
df_germany = df_germany[['year', 'lifeExp', 'pop', 'gdpPercap']]
df_countries =df[df['country'].isin(['Germany', 'Belgium', 'Denmark'])]

# creating the table
table = dash_table.DataTable(df_germany.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_germany.columns],
                               style_data={'color': 'white','backgroundColor': "#222222"},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'}, 
                                     style_table={ 
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                         'marginTop': 0, 'marginBottom': "30"}
                                     )


#creating the bar graph
fig = px.bar(df_countries, 
             x='year', 
             y='lifeExp',  
             color='country',
             barmode='group',
             height=300, title = "Germany vs Denmark & Belgium",)

fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", 
    #margin=dict(l=20, r=20, t=0, b=20)
)
    

graph = dcc.Graph(figure=fig)


#creating the line graph
fig2 = px.line(df_germany, x='year', y='lifeExp', height=300, title="Life Expectancy in Germany", markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)


#creating the map
fig3 = px.choropleth(df_countries, locations='iso_alpha', 
                    projection='natural earth', animation_frame="year",
                    scope='europe',  
                    color='lifeExp', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.ice)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
graph3 = dcc.Graph(figure=fig3)


# using the app with radio item
app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server

radio= dcc.RadioItems(id="countries",options=['Germany', 'Belgium', 'Denmark'], value="Germany", 
                      inline=True, style ={'paddingLeft': '30px'})


app.layout = html.Div([html.H1('Gap Minder Analysis of Germany', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("Using the gapminder data we take a look at Germany's profile"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('Germany', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 table, radio, graph,  graph2, graph3])
                      ])


@callback(
    Output(graph, "figure"), 
    Input("countries", "value"))

#let's also define discrete colors for each bar, so we can distinguish them easily, everytime we change our selection

def update_bar_chart(country): 
    mask = df_countries["country"]==(country)
    fig =px.bar(df_countries[mask], 
             x='year', 
             y='lifeExp',  
             color='country',
             color_discrete_map = {'Germany': '#7FD4C1', 'Denmark': '#8690FF', 'Belgium': '#F7C0BB'},
             barmode='group',
             height=300, title = "Germany vs Denmark & Belgium",)
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

    return fig 



if __name__ == "__main__":
    app.run_server()
