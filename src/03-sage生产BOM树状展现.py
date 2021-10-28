#coding:utf-8

import pandas as pd
import dash
from dash import html,dcc,Output,Input
import dash_bootstrap_components as dbc
import dash_tabulator
from textwrap import dedent as d
import json
import plotly.express as px

"""
https://github.com/preftech/dash-tabulator#usage

"""

#Load BOM
df = pd.read_excel(r"C:\Users\Administrator\Desktop\P102060300025(1).xlsx",
                   header=5,
                   skipfooter=6)
# print(df[df[ "级别" ] == 1])
# print(df.columns)

# 3rd party js to export as xlsx
external_scripts = ['https://oss.sheetjs.com/sheetjs/xlsx.full.min.js',
                    ]

# bootstrap css
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css']

# initialize your dash app as normal
app = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

styles = {
            'pre': {
                'border': 'thin lightgrey solid',
                'overflowX': 'scroll'
            }
        }

# Setup some columns
# This is the same as if you were using tabulator directly in js
# Notice the column with "editor": "input" - these cells can be edited
# See tabulator editor for options http://tabulator.info/docs/4.8/edit
columns = [
                { "title": "物料名称", "field": "物料名称", "width": 150, "headerFilter":True, "editor":"input","frozen":True},
                { "title": "层级", "field": "层级", "hozAlign": "left",  },#"formatter": "progress"
                { "title": "物料编码", "field": "物料编码", "hozAlign": "left",  },#"formatter": "progress"
                { "title": "规格", "field": "规格", "hozAlign": "left",  },#"formatter": "progress"
              ]

# Setup some data
## 如果是采用dataframe,须改成以下数据结构
data = [
                {"id":1, "物料名称":"S13-M-80/10", "层级":"0","物料编码":"S13-M-80/10","规格":"80kVA","_children":[
                    {"id":2, "物料名称":"器身", "层级":"1","物料编码":"5QB-700-20603ZJ-1","规格":"80kVA","_children":[
                        {"id":3, "物料名称":"铁心", "层级":"2","物料编码":"5QB-640-20603ZJ-1","规格":"80kVA",},
                        {"id":4, "物料名称":"高压绕组", "层级":"2","物料编码":"6QB-600-20603ZJ-1","规格":"80kVA","_children":[
                            {"id":5, "物料名称":"低压绕组", "层级":"3","物料编码":"6QB-600-20603ZJ-2","规格":"80kVA","_children":[
                                {"id":6, "物料名称":"纸包铜扁线", "层级":"4","物料编码":"M01020600000307","规格":"ZB-0.45-3.35×6.00/3.80×6.45",},
                            ]},
                         ]},
                    ]},
                ]},
       ]


# Additional options can be setup here
# these are passed directly to tabulator
# In this example we are enabling selection
# Allowing you to select only 1 row
# and grouping by the col (color) column

## 说明:通过groupby可以变换表格最左边的树状结构,
options = { "selectable":1,"dataTree":True,"selectableRangeMode":"click",} # "groupBy": ["col"],


# downloadButtonType
# takes
#       css     => class names
#       text    => Text on the button
#       type    => type of download (csv/ xlsx / pdf, remember to include appropriate 3rd party js libraries)
#       filename => filename prefix defaults to data, will download as filename.type

downloadButtonType = {"css": "btn btn-primary", "text":"下载", "type":"xlsx"}


# clearFilterButtonType
# takes
#       css     => class names
#       text    => Text on the button
clearFilterButtonType = {"css": "btn btn-outline-dark", "text":"清除筛选"}


# Add a dash_tabulator table
# columns=columns,
# data=data,
# Can be setup at initialization or added with a callback as shown below
# thank you @AnnMarieW for that fix


app.layout = dbc.Container([
    dash_tabulator.DashTabulator(
        id='tabulator',
        #columns=columns,
        #data=data,
        options=options,
        downloadButtonType=downloadButtonType,
        clearFilterButtonType=clearFilterButtonType,
    ),
    html.Div(id='output'),
    dcc.Interval(
                id='interval-component-iu',
                interval=1*10, # in milliseconds
                n_intervals=0,
                max_intervals=0
            ),
])


# dash_tabulator can be populated from a dash callback
@app.callback([ Output('tabulator', 'columns'),
                Output('tabulator', 'data')],
                [Input('interval-component-iu', 'n_intervals')])
def initialize(val):
    return columns, data

# dash_tabulator can register a callback on rowClicked,
#   cellEdited => a cell with a header that has "editor":"input" etc.. will be returned with row, initial value, old value, new value
# dataChanged => full table upon change (use with caution)
# dataFiltering => header filters as typed, before filtering has occurred (you get partial matching)
# dataFiltered => header filters and rows of data returned
# to receive a dict of the row values
@app.callback(Output('output', 'children'),
    [Input('tabulator', 'rowClicked'),
    Input('tabulator', 'cellEdited'),
    Input('tabulator', 'dataChanged'),
    Input('tabulator', 'dataFiltering'),
    Input('tabulator', 'dataFiltered')])
def display_output(row, cell, dataChanged, filters, dataFiltered):
    print(row)
    print(cell)
    print(dataChanged)
    print(filters)
    print(dataFiltered)
    return 'You have clicked row {} ; cell {}'.format(row, cell)

if __name__ == '__main__':
    app.run_server(debug=True)
