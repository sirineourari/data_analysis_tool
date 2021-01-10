# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:49:48 2020

@author: hp
"""
import dash
from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import dash_table
from dash.dependencies import Input, Output,State
from django.contrib.auth.models import User
import xlsxwriter 
from xlsxwriter  import Workbook
import xlrd 
app = DjangoDash('Simple')

df = pd.read_excel(r'C:\Users\hayfa\Downloads\projet1\dashapp\dash_apps\finished_apps\pcd.xlsx',sep = ',')
workbook = xlrd.open_workbook(r"C:\Users\hayfa\Downloads\projet1\dashapp\dash_apps\finished_apps\fiche_des_notes_du_form.xls")
PAGE_SIZE = 5
m=df.columns[:6]
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list
def const(m):
    l=[]
    for i in m :
        l.append(html.P(i))
        l.append(dcc.Dropdown(id=i, options=get_options(df[i].unique()),multi=True))
    l.append(html.P('Choisissez les questions dont vous vlouez voir l\'analyse:'))
    l.append(dcc.Dropdown(id='questselector', options=get_options([i for i in df.columns[6:]]),
                                      multi=False , #value=df.columns[7]
                                      #style={'backgroundColor': '#1E1E1E'},
                                      #className='modeselector'
                                                      ))
        
        
    return l
    
def lire(q):
    SheetNameList = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(SheetNameList[0])
    num_rows = worksheet.nrows 
    num_cells = worksheet.ncols 
    curr_row = 1 
    while curr_row < num_rows:
        cell_value = worksheet.cell_value(curr_row,1)
        if (cell_value == q):
            a=curr_row-1
            cell_value = worksheet.cell_value(a,1)
            return cell_value
        curr_row += 1
    
app.layout = html.Div(
    children=[
        dcc.Store(id = 'memory'),    
        html.Div(id = 'table-box'),       
        html.Div(className='colGauche',id='table',style={
                                        'right': '0%', 
                                        'background-image': 'linear-gradient(180deg, #fff, #ddd 40%, #ccc)',
                                        'border': '1px solid',
                                        'width':'83%',
                                        'height':'28%',
                                        'position':'absolute',
                                        
                                            }),
        html.Div(dcc.Graph(id='example-graph',
                    className = "four_columns"),style={
                        'right': '0%',
                        
                        'width':'85%',
                        'height':'32%',
                        'position':'absolute',
                        'bottom':'29%',
                    }),
        html.Div(className='colDroite',children=[html.Div(children=const(m),style={
                
                'background-color':'lightgreen',
                'border': '1px solid',
                'width':'15%',
                'height':'100%',
                'position':'absolute',

                'background-image': 'linear-gradient(180deg, #fff, #ddd 40%, #ccc)',

                }
                   )])
        
        ])
    
@app.expanded_callback(Output('table', 'children'),[Input(i, 'value') for i in m ])
def update_output(an,sm,niv,cl,mod,ens, *args,**kwargs):
    da= kwargs['user']
    if da.username=='admin':
        dff=df
    else:
        dff=df[df['enseignant']==da.username]
    if an:
        for i in an:
            dff=df[(df[m[0]].isin(an))]
    if sm:
        for j in sm :
            dff=dff[(dff[m[1]].isin(sm))]
    if niv:
        for k in niv:
            dff=dff[(dff[m[2]].isin(niv))]
    if cl:
        for l in cl:
            dff=dff[(dff[m[3]].isin(cl))]
    if mod:
        for s in mod:
            dff=dff[(dff[m[4]].isin(mod))]
    if ens:
        for h in ens:
            dff=dff[(dff[m[5]].isin(ens))]
    return dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable":False, "selectable": False } for i in dff.columns
        ],
        data=dff.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 4,
    )
@app.expanded_callback(
    Output('example-graph', 'figure'),
    [Input(i, 'value') for i in m ]+[Input('questselector', 'value')
     ])
def update_graph(an,sm,niv,cl,mod,ens,qu, *args,**kwargs):
    da= kwargs['user']
    if da.username=='admin':
        dff=df
    else:
        dff=df[df['enseignant']==da.username]
    t=None
    x=None
    y=None
    if an:
        for i in an:
            dff=df[(df[m[0]].isin(an))]
    if sm:
        for j in sm :
            dff=dff[(dff[m[1]].isin(sm))]
    if niv:
        for k in niv:
            dff=dff[(dff[m[2]].isin(niv))]
    if cl:
        for l in cl:
            dff=dff[(dff[m[3]].isin(cl))]
    if mod:
        for s in mod:
            dff=dff[(dff[m[4]].isin(mod))]
    if ens:
        for h in ens:
            dff=dff[(dff[m[5]].isin(ens))]    
    if qu!=None and mod:
        x=[i for i in dff[qu].unique()]
        y=[dff[qu].value_counts()[i] for i in dff[qu].unique()]
        t=lire(qu)

    return{
        'data': [ {'x':x,
                   'y':y,
                   'type': 'bar'}],
        'layout':
                {'title':t}
            }
    

if __name__ == '__main__':
    app.run_server(debug=True)
