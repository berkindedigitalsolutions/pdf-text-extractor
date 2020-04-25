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
            html.Div(id="output-excel"),
            html.Div(
                className = "col-8",
                style={
                        "width": "600px",
                        "height": "600px",
                        "border": "1px solid red",

                    },
                id="pdf-output")
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
    print(type(images))
    print(images)
    encoded = pil_to_b64_dash(images[0])

    return html.Div([

        html.Img(
            src=encoded.decode('utf-8'),

        ),
        html.Hr(),
    ])

############################################ Uploaded Excel ######################################################
@app.callback(Output('pdf-output', 'children'),
              [Input('pdf-upload', 'contents')],
              [State('pdf-upload', 'filename'),
               State('pdf-upload', 'last_modified')])
def show_coa(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_coa_contents(list_of_contents, list_of_names, list_of_dates)]

        return children

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

############################################ Excel Callback ######################################################
@app.callback(Output('output-excel', 'children'),
              [Input('upload-excel', 'contents')],
              [State('upload-excel', 'filename'),
               State('upload-excel', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_hot_reload=True)