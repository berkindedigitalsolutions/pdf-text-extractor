import base64
import os
from urllib.parse import quote as urlquote
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#from users import users_info
from flask import Flask, send_from_directory
import json
import dash_daq as daq
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from layouts import layout
import dash_bootstrap_components as dbc

########### Define your variables

tabtitle='PDF to Text'

UPLOAD_DIRECTORY = "/project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

server= Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)

@server.route("/download/<path:path>")
def download(path):
    #Serve a file from the upload directory
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

#server = app.server
app.title=tabtitle

app.layout = layout

#saving file locally

def save_file(name,content):
    #Decode and store a file uploaded with Plotly Dash
    data = content.encode("utf-8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY,name),"wb") as fp:
        fp.write(base64.decodebytes(data))

# uploading files to the list

def uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    #Create an anchor element that downloads the file from the app

    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

@app.callback(
    Output("file-list","children"),
    [Input("upload-data","filename"),
    Input("upload-data","contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=True)
