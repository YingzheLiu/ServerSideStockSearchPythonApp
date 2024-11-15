# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, request, jsonify, abort, render_template
from datetime import *
from dateutil.relativedelta import *
import requests

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
application = Flask(__name__)

BASE_URL = "https://finnhub.io/api/v1"
API_KEY = 'c8a9lvaad3iasddfdpr0'

SAMPLE_RESPONSE = {
  "c": [
    217.68,
    221.03,
    219.89
  ],
  "h": [
    222.49,
    221.5,
    220.94
  ],
  "l": [
    217.19,
    217.1402,
    218.83
  ],
  "o": [
    221.03,
    218.55,
    220
  ],
  "s": "ok",
  "t": [
    1569297600,
    1569384000,
    1569470400
  ],
  "v": [
    33463820,
    24018876,
    20730608
  ]
}

@application.route('/company', methods=['GET'])
def fetchCompany():
    print('fetchCompany()')
    ticker = request.args.get('ticker', 'none').upper()
    print('ticker: ' + ticker)
    payload = {'symbol': ticker, 'token': API_KEY}
    company = requests.get(BASE_URL + '/stock/profile2', params=payload)
    if company is None:
        abort(404)
    print(company.json())
    return jsonify(company.json())

@application.route('/stock', methods=['GET'])
def fetchStock():
    print('fetchStock()')
    ticker = request.args.get('ticker', 'none').upper()
    print('ticker: ' + ticker)
    payload = {'symbol': ticker, 'token': API_KEY}
    stock = requests.get(BASE_URL + '/quote', params=payload)
    if stock is None:
        abort(404)
    print(stock.json())
    return jsonify(stock.json())

@application.route('/recommendation', methods=['GET'])
def fetchRecommendation():
    print('fetchRecommendation()')
    ticker = request.args.get('ticker', 'none').upper()
    print('ticker: ' + ticker)
    payload = {'symbol': ticker, 'token': API_KEY}
    recommendation = requests.get(BASE_URL + '/stock/recommendation', params=payload)
    if recommendation is None:
        abort(404)
    print(recommendation.json())
    return jsonify(recommendation.json())

@application.route('/stockcandles', methods=['GET'])
def fetchStockCandles():
    print('fetchStock()')
    ticker = request.args.get('ticker', 'none').upper()
    NOW = datetime.now(timezone.utc)
    # print(NOW.replace(tzinfo=ZoneInfo('America/Los_Angeles')).timestamp())
    TO = int(round(datetime.timestamp(NOW)))
    print(TO)
    FROM = int(round(datetime.timestamp(NOW + relativedelta(months=-6, days=-1))))
    print(FROM)
    payload = {'symbol': ticker, 'resolution': 'D', 'from': FROM, 'to': TO, 'token': API_KEY}
    # stock_candles = requests.get(BASE_URL + '/stock/quote', params=payload)
    stock_candles = SAMPLE_RESPONSE
    return jsonify(stock_candles)

@application.route('/companynews', methods=['GET'])
def fetchNews():
    ticker = request.args.get('ticker', 'none').upper()
    TODAY = date.today()
    print(TODAY)
    FROM = TODAY + relativedelta(days=-30)
    print(FROM)
    payload={'symbol': ticker, 'from': FROM, 'to': TODAY, 'token': API_KEY} #from=BEFORE_30&to=TODAY
    news = requests.get(BASE_URL + '/company-news', params=payload)
    return jsonify(news.json())

@application.route('/')
def homepage(): 
    return render_template("index.html")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the application. You
    # can configure startup instructions by adding `entrypoint` to application.yaml.
    application.static_folder = 'static'
    application.run(host='0.0.0.0', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]