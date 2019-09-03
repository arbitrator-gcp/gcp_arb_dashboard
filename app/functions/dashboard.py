from flask import Flask, render_template, make_response
import json

def db(request):


    # API query should return:
    # 1. inidividuals
    # 2. hourly and minutely
    # single call, or combined?
    # initial - combined, can split later maybe

    file_js = open("static/js/main.js","r")  
    main_js = file_js.read()

    with open("static/data/data.json", "r") as f:
        data = json.load(f)

    rate = data["rate"]
    luno = data["luno"]
    kraken = data["kraken"]
    arb = data["arb"]
    hourly = data["hourly"]
    minutely = data["minutely"]
    
    # Hourly line chart
    h_chart_id = "h_chart_id"
    h_chart = {"renderTo": h_chart_id, "type": "spline", "height": 350}
    h_series = [{"name": "Luno", "data": hourly["luno"]},{"name": "Kraken", "data": hourly["kraken"]}]
    h_title = {"text": "Hourly BTC price"}
    h_xAxis = {"title": {"text": "Date and time"}, "type": "datetime", "labels": {"overflow": "justify"}}
    h_yAxis = {"title": {"text": "BTC Price (ZAR)"}, "lineWidth": 1}
    h_plotOptions = {"spline": {
        "marker": {"enabled": "false"},
        "pointInterval": 3600000,
        "pointStart": "Date.parse(" + min(hourly['hours']) + ")"}}

    h_params = {"h_chart_id":"hourly_line", "h_chart":h_chart, "h_series":h_series, "h_title":h_title, "h_xAxis":h_xAxis, "h_yAxis":h_yAxis, "h_plotOptions":h_plotOptions}

    # CORS stuff: https://cloud.google.com/functions/docs/writing/http
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            # 'X-Content-Type-Options': 'text/html',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        # 'X-Content-Type-Options': 'text/html',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*'
    }
    # r
    resp = make_response(render_template("index.html", js=main_js, msg="hello", **h_params))
    # r.headers.set('Access-Control-Allow-Origin', "*")
    # resp.headers.set('Access-Control-Allow-Origin', '*')
    # resp.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    # resp.headers.set('Access-Control-Allow-Headers', 'Content-Type')
    return(resp, 200, headers)