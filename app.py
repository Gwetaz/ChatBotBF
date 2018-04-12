# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
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

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
 if   req.get("result").get("action") == "yahooWeatherForecast":
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

 elif req.get("result").get("action") == "yahooWeatherFivecast":
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery2(req)
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult2(data)
    return res

 else:
        return {}


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

def formatD(dateu):
    
    sousa = dateu[8:10]
    sousb = dateu[0:4]
    sousc= dateu[5:7]
    
    choices = {"01": "Jan","02":"Fev","03":"Mar", "04" : "Apr", "05" : "May","06":"Jun"}
    result = choices.get(sousc, 'default')
    
    return sousa+" "+result+" "+sousb

def makeYqlQuery2(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    date = formatD(parameters.get("date"))
    if city is None:
        return None
#err1?
    return "select item.forecast.date,location.city,item.forecast.text,item.forecast.high,item.forecast.low from weather.forecast where woeid in (select woeid from geo.places(1) where text=' " + city + " ') and item.forecast.date = '"+ date + "' "
    
def conv(tempe):    
    
    tempe = float(tempe)
    tempe = tempe - 32
    tempe = tempe / (9/5)
    tempe = round(tempe,1)
    tempe = str(tempe)
    return tempe

def moy(var,var2):
    
    var = float(var)
    var2 = float(var2)
    var = (var + var2) / 2
    var = round(var,1)
    var = str(var)
    return var

def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}
    


    # print(json.dumps(item, indent=4))
    test =  conv(condition.get('temp'))
    speech = "Aujourd'hui la météo à " + location.get('city') + " est : " + condition.get('text') + \
             ", et la température est de " + test + " " + "°C \n Tu peux demander un autre jour de la semaine !"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeWebhookResult2(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}
  

    item = channel.get('item')
    location = channel.get('location')
    city = location.get('city')
    forecast = item.get('forecast')

  
    


    # print(json.dumps(item, indent=4))
    test =  conv(moy(forecast.get('high'),forecast.get('low')))
    speech = "la météo de "+ city + " le "+forecast.get('date')+" est : " + forecast.get('text') + \
             ", et la température est de " + test + " " + "°C \n Tu peux me donner un nouveau jour ou redonne moi une ville  !"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
