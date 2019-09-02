from flask import Flask, render_template, make_response
import json

def dashboard(request):


    # API query should return:
    # 1. inidividuals
    # 2. hourly and minutely
    # single call, or combined?
    # initial - combined, can split later maybe
    # with open("static/data/data.json", "r") as f:
    #     data = json.load(f)

    # rate = data["rate"]
    # luno = data["luno"]
    # kraken = data["kraken"]
    # arb = data["arb"]
    # hourly = data["hourly"]
    # minutely = data["minutely"]
    
    
    # chart = {"renderTo": "chart_ID", "type": "line", "height": 350,}

    # series = [{"name": "Luno", "data": hourly["luno"]}, {"name": "Kraken", "data": hourly["kraken"]}]
    # title = {"text": "Hourly BTC price"}
    # xAxis = {"title": {"text": "Date and time"}}
    # yAxis = {"title": {"text": "BTC Price (ZAR)"}}
    # plotOptions = {"series": {"label": {"connectorAllowed": "false"},"pointStart": min(hourly["hours"])}}

    # CORS stuff: https://cloud.google.com/functions/docs/writing/http
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': 'Authorization',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true',
            'Origin': 'https://us-central1-arbitrator-251115.cloudfunctions.net'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Content-Type':'text/html',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Origin': 'https://us-central1-arbitrator-251115.cloudfunctions.net'
    }
    # r
    # resp = make_response(render_template("index.html", msg="hello", chartID="chart_ID", chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis))
    # r.headers.set('Access-Control-Allow-Origin', "*")
    # resp.headers.set('Access-Control-Allow-Origin', '*')
    # resp.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    # resp.headers.set('Access-Control-Allow-Headers', 'Content-Type')
    return(make_response(render_template("hello.html", msg="hello"), 200, headers))