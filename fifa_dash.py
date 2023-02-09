import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import dash_table
from dash.dependencies import Input, Output, State

position_model=pickle.load(open('position_predict.sav', 'rb'))
over_model=pickle.load(open('over_predict.sav', 'rb'))

external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout=html.Div(
    children=[
        html.H1('MAKE YOUR OWN FIFA 20 RATINGS'),
        html.Div(children='by diushalimi'),
        html.Div(children=[html.Label('Age : '), dcc.Input(id='age', type='number')]),
        html.Div(children=[html.Label('Height : '), dcc.Input(id='height', type='number')]),
        html.Div(children=[html.Label('Weight : '), dcc.Input(id='weight', type='number')]),
        html.Div(children=[html.Label('Pace : '), dcc.Input(id='pace', type='number')]),
        html.Div(children=[html.Label('Dribble : '), dcc.Input(id='dribbling', type='number')]),
        html.Div(children=[html.Label('Shoot : '), dcc.Input(id='shooting', type='number')]),
        html.Div(children=[html.Label('Pass : '), dcc.Input(id='passing', type='number')]),
        html.Div(children=[html.Label('Defence : '), dcc.Input(id='defending', type='number')]),
        html.Div(children=[html.Label('Physics : '), dcc.Input(id='physicality', type='number')]),
        html.Div(children=[html.P('Preferred Foot'), dcc.Dropdown(value='',id='pref_foot_Right', options=[{'label':'Right','value':1},
                                                                                                        {'label':'Left','value':0}])]),
        html.Div(children=[html.P('Skill Moves'), dcc.Dropdown(value='',id='skill_moves', options=[{'label':i,'value':i} for i in range(1,6)])]),
        html.Div(children=[html.P('Weak Foot'), dcc.Dropdown(value='',id='weak_foot', options=[{'label':i,'value':i} for i in range(1,6)])]),
        html.Div(id='prediksi')
    ]
)

@app.callback(
    Output(component_id='prediksi', component_property='children'),
    [Input(component_id='age', component_property='value'),
    Input(component_id='height', component_property='value'),
    Input(component_id='weight', component_property='value'),
    Input(component_id='pace', component_property='value'),
    Input(component_id='dribbling', component_property='value'),
    Input(component_id='passing', component_property='value'),
    Input(component_id='shooting', component_property='value'),
    Input(component_id='defending', component_property='value'),
    Input(component_id='physicality', component_property='value'),
    Input(component_id='pref_foot_Right', component_property='value'),
    Input(component_id='skill_moves', component_property='value'),
    Input(component_id='weak_foot', component_property='value')]
)

def prediksi(age, height, weight, pace, dribbling, passing, shooting, defending, physicality, pref_foot_Right, skill_moves, weak_foot):
    posisi=position_model.predict(np.array([pace, dribbling, passing, shooting, defending, physicality, pref_foot_Right, skill_moves, weak_foot]).reshape(1,-1))
    over=over_model.predict(np.array([pace, dribbling, passing, shooting, defending, physicality, skill_moves, weak_foot, age, height, weight]).reshape(1,-1))
    return 'Congratulation! You are suitable in position area {} with {} overall'.format(posisi[0], over[0])

if __name__=='__main__':
    app.run_server(debug=True)