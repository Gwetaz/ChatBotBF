# -*- coding:utf8 -*-
# !/usr/bin/env python


from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sys


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
baseurl = "https://brittany-ferries-holidays-api-ferries-apis.ngpb.io/v1/"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print (sys.version)
    print("Request:")
    print("test Avant dumps")
    print(json.dumps(req, indent=4))
    
    print("test Avant processReq")
    print(req)

    res = processRequest(req)
    
    print("test Apres processReq")
    print(res)
    

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
 if   req.get("queryResult").get("action") == "TraverserVV":
    
    print("avant makeYql")
    yql_query = makeYqlQuery(req)
    yql_url = baseurl +"crossings?"+yql_query
    print(yql_url)
    headers = {}
    headers['Authorization'] = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaG9ydEJyZWFrcyIsInJvbGVzIjoiUk9MRV9DVVNUT01FUiIsImlzcyI6IkJyaXRhbnkgRmVycmllcyIsImlhdCI6MTUyMjc0MjEwNCwianRpIjoiMjcxYzA2ZGMtOGQ4YS00YTZmLWE1ZDYtMDRiZThlNzEyMmU4In0.RD4zhr5Ve2Vkay-_6_ZRzKxgbjnG6B1YKZS3bazS9vs"
    URL = Request(yql_url,headers = headers)
    print(URL)
    result = urlopen(URL)
    lu = result.read()
    data = json.loads(lu)
    print('alolemonde')
    res = makeWebhookResult(data,req)
    print("apresWebhook")
    print(res)
    return res



 else:
        return {}


def makeYqlQuery(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    depart = CodePort(parameters.get("dpart"))
    print(depart)
    contexttab = result.get("outputContexts")
    context = contexttab[0].get("parameters")
    print(context)
    desti = CodePort(context.get("PortsBAI"))
    print(desti)
    date = parameters.get("date")
    dateMod = urlencode({ 'q' : date})[2:35]
    print(dateMod)

    return "departure_ports="+depart+"&arrival_ports="+desti+"&date_from="+dateMod



def makeWebhookResult(data,req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    contexttab = result.get("outputContexts")
    context = contexttab[0].get("parameters")
    desti = context.get("PortsBAI")
    
    data = data.get('data')
    if data is None:
        return {}
    ship = data[0].get('ship_name')
    if ship is None:
        return {}
    dateD = data[0].get('departure').get('datetime')
    
    
    speech = " Le "+ship+" prend la mer pour "+desti+" le "+dateD[8:10]+"/"+dateD[5:7]+" à "+dateD[11:16]+"h réserver maintenant !"
    print(speech)
    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
           "simpleResponses": [
            {
              "textToSpeech": speech
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "linkOutSuggestion": {
          "destinationName": "Je réserve ",
          "uri": "brittany-ferries.fr/510?AccountNo=&ferry=ferryonly&journeyType=return&journeyTypeState=&FCONsubmission=true&frmOGroup=9&frmORoute=&frmODay="+date[8:10]+"&frmOMonthYear=&frmOMonth="+date[5:7]+"&frmOYear="+date[0:5]+"frmOMonthYearRestore=&frmODayRestore=&frmIGroup=5&frmIRoute=&frmIDay=frmIMonthYear=frmIMonth=frmIYear=frmIMonthYearRestore=&frmIDayRestore=&submit=Je+réserve"
        }
      }
     ]
    }


def CodePort(por):
    choices = {"Le Havre":"FRLEH","Portsmouth":"GBPME","Bilbao":"ESBIO","Plymouth":"GBPLY","Cork":"IEORK","Roscoff":"FRROS","Poole":"GBPOO","Cherbourg":"FRCER","St Malo":"FRSML","Ouistrham":"FROUI","Santander":"ESSDR"}
    result = choices.get(por, '')
    return result

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host='0.0.0.0')
