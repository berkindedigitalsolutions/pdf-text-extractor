  
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#from users import users_info
import flask
import json
import dash_daq as daq
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
import os 
import dash_bootstrap_components as dbc


def createUpload(uploadid):
    return dcc.Upload(
        id=uploadid,
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '20px auto'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )


file_upload = createUpload("file-upload")



layout = html.Div(children=[
    html.Div(
        className ="container text-center mt-5", 
        children=[
            html.H1(className="m-5", children="PDF Extractor"),
            html.H2("Upload"),
            file_upload,
            html.H2("File List"),
    ])
 ])



