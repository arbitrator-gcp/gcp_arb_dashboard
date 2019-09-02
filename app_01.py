from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index(chartID = "chart_ID", chart_type = "bar", chart_height = 350):
	# API query should return:
	# 1. inidividuals
	# 2. hourly and minutely
	# single call, or combined?
	# initial - combined, can split later maybe
	with open("static/data/data.json", "r") as f:
		data = json.load(f)
	rate = data["rate"]
	luno = data["luno"]
	kraken = data["kraken"]
	arb = data["arb"]
	hourly = data["hourly"]
	minutely = data["minutely"]
	

	chart = {"renderTo": chartID, "type": "line", "height": chart_height,}

	series = [{"name": "Luno", "data": hourly["luno"]}, {"name": "Kraken", "data": hourly["kraken"]}]
	title = {"text": "Hourly BTC price"}
	xAxis = {"title": {"text": "Date and time"}}
	yAxis = {"title": {"text": "BTC Price (ZAR)"}}
	plotOptions = {"series": {"label": {"connectorAllowed": "false"},"pointStart": min(hourly["hours"])}}
	return render_template("index.html", chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

if __name__ == "__main__":
	app.run(debug = True, host="0.0.0.0", port=8080, passthrough_errors=True)