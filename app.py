import base64
import datetime
import io
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go

import flask
import json

from pdf2image import convert_from_path, convert_from_bytes
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
            html.Div(
                className="row", children = [
                    html.Div(className ="col-6", children = [
                    html.H2(className="m-5", children ="Upload PDF"),
                    dcc.Upload(
                        id="pdf-upload",
                        children=html.Div(
                            ["Drag and drop or click to select a file to upload."]
                        ),
                        style={
                            "width": "70%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "20px auto",
                        },
                        multiple=False,
                    ),
            ]),
                html.Div(className ="col-6", children = [
                        html.H2(className="m-5", children ="Upload Excel"),
                        dcc.Upload(
                            id="upload-excel",
                            children=html.Div(
                                ["Drag and drop or click to select a file to upload."]
                            ),
                            style={
                                "width": "70%",
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
                ]),
            ]),

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
            html.Div(id="pdf-output")
])

def pil_to_b64_dash(im):
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return bytes("data:image/jpeg;base64,", encoding='utf-8') + img_str

def parse_coa_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    
    decoded = base64.b64decode(content_string)
    
    images = convert_from_bytes(decoded)
    
    encoded = pil_to_b64_dash(images[0])

    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=encoded.decode('utf-8')),
        html.Hr(),
    ])

@app.callback(Output('pdf-output', 'children'),
              [Input('pdf-upload', 'contents')],
              [State('pdf-upload', 'filename'),
               State('pdf-upload', 'last_modified')])
def show_coa(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_coa_contents(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_hot_reload=True)