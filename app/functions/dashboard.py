from flask import Flask, render_template, make_response
import json
from google.cloud import firestore

def dashboard(request):
    # queries to get most up to date values

    fs_client = firestore.Client()
    q_fs_rate = fs_client.collection(u'rates').order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    curr_rate = list({doc.to_dict()["EUR"] for doc in q_fs_rate})[0]
    # curr_ts = list({doc.to_dict()["timestamp"] for doc in q_fs_rate})[0]

    q_fs_kraken = fs_client.collection(u'kraken').order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    curr_kraken = list({doc.to_dict()["result_price_last"] for doc in q_fs_kraken})[0] * (1/curr_rate)

    q_fs_luno = fs_client.collection(u'luno').order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    curr_luno = list({doc.to_dict()["result_price_last"] for doc in q_fs_luno})[0]

    curr_data = {"luno":round(curr_luno,2), "kraken":round(curr_kraken,2), "arb":round(((curr_luno-curr_kraken)/curr_kraken)*100, 2), "rate":round(curr_rate, 2)  }


    file_js = open("static/js/main.js","r")  
    main_js = file_js.read()

    # API query should return:
    # get most recent FS cache record
    q_fs = fs_client.collection(u'cache').order_by(u'timestamp_ms', direction=firestore.Query.DESCENDING).limit(1).get()
    # dict_tmp = {doc.to_dict()["kraken"] for doc in q_fs}
    series = json.dumps({"data": {key:doc.to_dict()[key] for key in doc.to_dict().keys()} for doc in q_fs})["data"]["series"]

    # with open("static/data/data2.json", "r") as f:
    #     data = json.load(f)
    # series = data["data"]["series"]
    
    # Hourly prices line chart
    h_prices_id = "h_prices_id"
    h_prices_chart = {"type": "spline", "height": 350}
    h_prices_data = [{"name":"Kraken", "data":[[series[i]["timestamp_ms"], series[i]["kraken"]] for i in range(len(series))]},
                     {"name":"Luno", "data":[[series[i]["timestamp_ms"], series[i]["luno"]] for i in range(len(series))]}]
    h_prices_title = {"text": "Hourly BTC price"}
    h_prices_xAxis = {"type": "datetime"}
    h_prices_yAxis = {"title": {"text": "BTC Price (ZAR)"}, "lineWidth": 1}
    h_prices_params = {"h_prices_idv":h_prices_id, "h_prices_chart":h_prices_chart, "h_prices_data":h_prices_data, "h_prices_title":h_prices_title, 
                       "h_prices_xAxis":h_prices_xAxis, "h_prices_yAxis":h_prices_yAxis}

    # Hourly Arbitrage chart
    h_arb_id = "h_arb_id"
    h_arb_chart = {"type": "spline", "height": 350}
    h_arb_data = [{"name":"Arbitrage", "data":[[series[i]["timestamp_ms"], series[i]["arb"]] for i in range(len(series))]}]
    h_arb_title = {"text": "Hourly Arbitrage (uncorrected)"}
    h_arb_xAxis = {"type": "datetime"}
    h_arb_yAxis = {"title": {"text": "Arbitrage (%)"}, "lineWidth": 1}
    h_arb_params = {"h_arb_idv":h_arb_id, "h_arb_chart":h_arb_chart, "h_arb_data":h_arb_data, "h_arb_title":h_arb_title, 
                    "h_arb_xAxis":h_arb_xAxis, "h_arb_yAxis":h_arb_yAxis}

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

    resp = make_response(render_template("index.html", js=main_js, msg="hello", **curr_data, **h_prices_params, **h_arb_params))
    return(resp, 200, headers)