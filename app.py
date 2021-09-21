from flask import Flask, render_template, url_for, request, redirect
import requests, json
from datetime import datetime
from dateutil.parser import parse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def Index():

    _filter = ""

    if request.method == 'POST':
        if request.form["Toggle"] == "All":
            _filter = ""
        elif request.form["Toggle"] == "IR":
            _filter = "type=ir"
        elif request.form["Toggle"] == "PR":
            _filter = "type=pr"
        elif request.form["Toggle"] == "Regulatory":
            _filter = "tag=:regulatory"
        elif request.form["Toggle"] == "Interim report":
            _filter = "tag=sub:report:interim"
        elif request.form["Toggle"] == "Annual report":
            _filter = "tag=sub:report:annual"
        elif request.form["Toggle"] == "Report archive":
            _filter = "tag=sub:report"
    
    req = requests.get("https://feed.mfn.se/v1/feed/3a920c14-5ffb-40b9-9ca5-889d038690f1.json?{}".format(_filter))
    news = req.json()["items"]

    for i in news:
        format_time = parse(i["content"]["publish_date"]).replace(tzinfo=None)
        i["content"]["publish_date"] = format_time

    return render_template('index.html', news=news)



@app.route("/view/", methods=['GET', 'POST'])
def View():
    keyword = request.args.get('press')

    req = requests.get("https://feed.mfn.se/v1/feed/3a920c14-5ffb-40b9-9ca5-889d038690f1.json?news-id={}".format(keyword))
    data = req.json()["items"][0]
    content_html = data["content"]["html"]

    return render_template('view.html', view=data, content=content_html)
