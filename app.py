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


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]



# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
#server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(className = "container text-center", children=
        [
            html.H1(className = "m-5", children="File Browser"),
            html.H2(className="m-5", children ="Upload Files"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to select a file to upload."]
                ),
                style={
                    "width": "50%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "20px auto",
                },
                multiple=True,
            ),
            html.H2(className="mb-5", children="File List"),
            html.Ul(id="file-list"),
            html.Button(
                id="btn-submit", 
                className="btn btn-primary m-5",                 
                style={
                        "width": "10%",
                        "height": "60px",
                        "font-size":"18px",
                        "textAlign": "center",
                        "margin": "20px auto",
                    },children="Run"),
            html.Div(id="btn-output")
])




if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_hot_reload=True)