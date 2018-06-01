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

#On prépare les connexions aux différentes API :
baseurl = "https://brittany-ferries-holidays-api-ferries-apis.ngpb.io/v1/"
baseurl2 = "https://brittany-ferries-holidays-api-hotels-proxy.ngpb.io/v1/" 

#Définition du webhook :
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True) #Récupération du JSON envoyé par Dialogflow
    print (sys.version)
    print("Request:")
    print("test Avant dumps")
    print(json.dumps(req, indent=4))
    
    print("test Avant processReq")
    print(req)

    res = processRequest(req) #On traite la requête 
    
    print("test Apres processReq")
    print(res)
    

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("queryResult").get("action") == "TraverserVV": # Traitement en fonction de l'action de l'intent dans DialofFlow
        print("avant makeYql")
        yql_query = makeYqlQuery(req) #Préparation de l'URL pour se connecter à une API 
        yql_url = baseurl +"crossings?"+yql_query
        print(yql_url)
        headers = {}
	#On ajoute au headers HTTP le bearer pour pouvoir utiliser l'API ( Clé d'accès)
        headers['Authorization'] = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaG9ydEJyZWFrcyIsInJvbGVzIjoiUk9MRV9DVVNUT01FUiIsImlzcyI6IkJyaXRhbnkgRmVycmllcyIsImlhdCI6MTUyMjc0MjEwNCwianRpIjoiMjcxYzA2ZGMtOGQ4YS00YTZmLWE1ZDYtMDRiZThlNzEyMmU4In0.RD4zhr5Ve2Vkay-_6_ZRzKxgbjnG6B1YKZS3bazS9vs"
        URL = Request(yql_url,headers = headers) # On crée la requête http à envoyer
        print(URL)
        result = urlopen(URL) #On envoit la requête à l'API et récupère le résultat dans une variable
        lu = result.read()
        data = json.loads(lu) #On convertit en JSON le résultat
        print('alolemonde')
        res = makeWebhookResult(data,req) #On prépare le message qui va être envoyé à l'utilisateur
        print("apresWebhook")
        print(res)
        return res
    
    elif req.get("queryResult").get("action") == "TraverserPortsmouth":
         print("avant makeYql")
         yql_query = makeYqlQuery2(req)
         yql_url = baseurl +"crossings?"+yql_query
         print(yql_url)
         headers = {}
         headers['Authorization'] = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaG9ydEJyZWFrcyIsInJvbGVzIjoiUk9MRV9DVVNUT01FUiIsImlzcyI6IkJyaXRhbnkgRmVycmllcyIsImlhdCI6MTUyMjc0MjEwNCwianRpIjoiMjcxYzA2ZGMtOGQ4YS00YTZmLWE1ZDYtMDRiZThlNzEyMmU4In0.RD4zhr5Ve2Vkay-_6_ZRzKxgbjnG6B1YKZS3bazS9vs"
         URL = Request(yql_url,headers = headers)
         print(URL)
         result = urlopen(URL)
         lu = result.read()
         data = json.loads(lu)
         print('alolemonde2')
         res = makeWebhookResult2(data,req)
         print("apresWebhook")
         print(res)
         return res
    
    elif req.get("queryResult").get("action") == "TraverserPoole":
         print("avant makeYql")
         yql_query = makeYqlQuery3(req)
         yql_url = baseurl +"crossings?"+yql_query
         print(yql_url)
         headers = {}
         headers['Authorization'] = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaG9ydEJyZWFrcyIsInJvbGVzIjoiUk9MRV9DVVNUT01FUiIsImlzcyI6IkJyaXRhbnkgRmVycmllcyIsImlhdCI6MTUyMjc0MjEwNCwianRpIjoiMjcxYzA2ZGMtOGQ4YS00YTZmLWE1ZDYtMDRiZThlNzEyMmU4In0.RD4zhr5Ve2Vkay-_6_ZRzKxgbjnG6B1YKZS3bazS9vs"
         URL = Request(yql_url,headers = headers)
         print(URL)
         result = urlopen(URL)
         lu = result.read()
         data = json.loads(lu)
         res = makeWebhookResult3(data,req)
         print("apresWebhook")
         print(res)
         return res
    
    elif req.get("queryResult").get("action") == "HorairePrecise":
         yql_query = makeYqlQuery4(req)
         print(yql_query)
         yql_url = baseurl +"crossings?"+yql_query
         print(yql_url)
         headers = {}
         headers['Authorization'] = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaG9ydEJyZWFrcyIsInJvbGVzIjoiUk9MRV9DVVNUT01FUiIsImlzcyI6IkJyaXRhbnkgRmVycmllcyIsImlhdCI6MTUyMjc0MjEwNCwianRpIjoiMjcxYzA2ZGMtOGQ4YS00YTZmLWE1ZDYtMDRiZThlNzEyMmU4In0.RD4zhr5Ve2Vkay-_6_ZRzKxgbjnG6B1YKZS3bazS9vs"
         URL = Request(yql_url,headers = headers)
         print(URL)
         result = urlopen(URL)
         print(result)
         lu = result.read()
         data = json.loads(lu)
         res = makeWebhookResult4(data,req)
         return res
    
    elif req.get("queryResult").get("action") == "Quartier":
         yql_query = makeQuartierQuery(req)
         print(yql_query)
         yql_url = baseurl2 +"hotels?"+yql_query
         print(yql_url)
         URL = Request(yql_url)
         print(URL)
         result = urlopen(URL)
         print(result)
         lu = result.read()
         data = json.loads(lu)
         res = makeWebhookQuartier(data)
         return res

    elif req.get("queryResult").get("action") == "Hotels":
         yql_query = makeHotelQuery(req)
         print(yql_query)
         yql_url = baseurl2 +"hotels?"+yql_query
         print(yql_url)
         URL = Request(yql_url)
         print(URL)
         result = urlopen(URL)
         print(result)
         lu = result.read()
         data = json.loads(lu)
         res = makeWebhookHotel(data)
         print(res)
         return res
	
    elif req.get("queryResult").get("action") == "Services":
         yql_query = makeHotelQuery(req)
         print(yql_query)
         yql_url = baseurl2 +"hotels?"+yql_query
         print(yql_url)
         URL = Request(yql_url)
         print(URL)
         result = urlopen(URL)
         print(result)
         lu = result.read()
         data = json.loads(lu)
         print(data)
         res = makeWebhookService(data,req)
         print(res)
         return res

    else:
           return {}


def makeYqlQuery(req):
    result = req.get("queryResult") #On récupère les données issus de DialogFlow
    parameters = result.get("parameters") #On stock ces données dans différentes variables
    contexttab = result.get("outputContexts")
    context = contexttab[1].get("parameters")
    print(context)
    desti = CodePort(context.get("PortPlym"))
    print(desti)
    depart = CodePort(context.get("PortsEnFrance"))
    print(depart)
    date = parameters.get("date")
    dateMod = urlencode({ 'q' : date})[2:35] #Urlencode permet d'afficher le bont format de date
    print(dateMod)
    #On peut créer le contenu de l'URL et le retourner
    return "departure_ports="+depart+"&arrival_ports="+desti+"&date_from="+dateMod

def makeYqlQuery2(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    contexttab = result.get("outputContexts")
    context = contexttab[1].get("parameters")
    print(context)
    desti = CodePort(context.get("PortPorts"))
    print(desti)
    depart = CodePort(context.get("PortsEnFrance"))
    print(depart)
    date = parameters.get("date")
    dateMod = urlencode({ 'q' : date})[2:35]
    print(dateMod)

    return "departure_ports="+depart+"&arrival_ports="+desti+"&date_from="+dateMod


def makeYqlQuery3(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    contexttab = result.get("outputContexts")
    context = contexttab[1].get("parameters")
    print(context)
    desti = CodePort(context.get("Portpool"))
    print(desti)
    depart = CodePort(context.get("PortsEnFrance"))
    print(depart)
    date = parameters.get("date")
    dateMod = urlencode({ 'q' : date})[2:35]
    print(dateMod)

    return "departure_ports="+depart+"&arrival_ports="+desti+"&date_from="+dateMod


def makeYqlQuery4(req):
    print("test")
    result = req.get("queryResult")
    param = result.get("parameters")
    desti = CodePort(param.get("PortEtranger"))
    print(desti)
    depart = CodePort(param.get("PortsEnFrance"))
    print(depart)
    ship = param.get("Ferry")
    date = param.get("date")
    dateMod = urlencode({ 'q' : date})[2:35]
    print(dateMod)

    return "departure_ports="+depart+"&arrival_ports="+desti+"&date_from="+dateMod


def makeQuartierQuery(req):
    print("test")
    result = req.get("queryResult")
    param = result.get("parameters")
    desti = param.get("QuartierLondres")
    print(desti)


    return "neighborhood_slug="+desti

def makeHotelQuery(req):
    print("entré dans makequery")
    result = req.get("queryResult")
    param = result.get("parameters")
    context = result.get("outputContexts")
    nom = param.get("Hotels")
    print(nom)
    if nom is None :  #Si le nom de l'hotel n'est pas dans les paramètres, on le cherche dans le contexte.
       print("rentré dans le if" )
       nom = urlencode({'name' : context[0].get("parameters").get("Hotels") }) 
    else : 
       nom = urlencode({'name' : nom})

    print(nom)
    return nom




def makeWebhookResult(data,req):
    
    result = req.get("queryResult") #On récupère les différentes informations dans le message précédent(req) ou dans le résultat de l'API (data) 
    parameters = result.get("parameters")
    contexttab = result.get("outputContexts")
    context = contexttab[1].get("parameters")
    desti = context.get("PortPlym")
    
    data = data.get('data')
    if data is None:
        return {}
    ship = data[0].get('ship_name')
    if ship is None:
        return {}
    dateD = data[0].get('departure').get('datetime')
    
    #On prépare le " Default Message qui sera envoyé à l'utilisateur"
    speech = " Le "+ship+" prend la mer pour "+desti+" le "+dateD[8:10]+"/"+dateD[5:7]+" à "+dateD[11:16]+"h , réservez maintenant !"
    print(speech)
    
    #Envois du message au format accepté par DialogFlow
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
      {#Possibilité d'utiliser les différents outils d'intégrations : (Ici Google Assistant et ces différents 'Rich Messages' 
        "platform": "ACTIONS_ON_GOOGLE",
        "linkOutSuggestion": {
          "destinationName": "Je réserve ",
          "uri": "https://www.brittany-ferries.fr/510?AccountNo=&ferry=ferryonly&journeyType=One+Way&journeyTypeState=One+Way&FCONsubmission=true&frmOGroup=9&frmORoute=&frmODay="+dateD[8:10]+"&frmOMonthYear=&frmOMonth="+dateD[5:7]+"&frmOYear="+dateD[0:4]+"&frmOMonthYearRestore=&frmODayRestore=&frmIRoute=&frmIMonth=&frmIYear=&frmIMonthYearRestore=&frmIDayRestore=&submit=Je+r%C3%A9serve "
        }
      }
     ]
    }



def makeWebhookResult2(data,req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    contexttab = result.get("outputContexts")
    context = contexttab[1].get("parameters")
    desti = context.get("PortPorts")
    
    data = data.get('data')
    if data is None:
        return {}
    ship = data[0].get('ship_name')
    if ship is None:
        return {}
    dateD = data[0].get('departure').get('datetime')
    
    
    speech = " Le "+ship+" prend la mer pour "+desti+" le "+dateD[8:10]+"/"+dateD[5:7]+" à "+dateD[11:16]+"h , réservez maintenant !"
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
          "uri": "https://www.brittany-ferries.fr/510?AccountNo=&ferry=ferryonly&journeyType=One+Way&journeyTypeState=One+Way&FCONsubmission=true&frmOGroup=9&frmORoute=&frmODay="+dateD[8:10]+"&frmOMonthYear=&frmOMonth="+dateD[5:7]+"&frmOYear="+dateD[0:4]+"&frmOMonthYearRestore=&frmODayRestore=&frmIRoute=&frmIMonth=&frmIYear=&frmIMonthYearRestore=&frmIDayRestore=&submit=Je+r%C3%A9serve "
        }
      }
     ]
    }



def makeWebhookResult3(data,req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    contexttab = result.get("outputContexts")
    context = contexttab[1].get("parameters")
    desti = context.get("Portpool")
    
    data = data.get('data')
    if data is None:
        return {}
    ship = data[0].get('ship_name')
    if ship is None:
        return {}
    dateD = data[0].get('departure').get('datetime')
    
    
    speech = " Le "+ship+" prend la mer pour "+desti+" le "+dateD[8:10]+"/"+dateD[5:7]+" à "+dateD[11:16]+"h , réservez maintenant !"
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
          "uri": "https://www.brittany-ferries.fr/510?AccountNo=&ferry=ferryonly&journeyType=One+Way&journeyTypeState=One+Way&FCONsubmission=true&frmOGroup=9&frmORoute=&frmODay="+dateD[8:10]+"&frmOMonthYear=&frmOMonth="+dateD[5:7]+"&frmOYear="+dateD[0:4]+"&frmOMonthYearRestore=&frmODayRestore=&frmIRoute=&frmIMonth=&frmIYear=&frmIMonthYearRestore=&frmIDayRestore=&submit=Je+r%C3%A9serve "
        }
      }
     ]
    }

def makeWebhookResult4(data,req):
    
    result = req.get("queryResult")
    param = result.get("parameters")
    desti = param.get("PortEtranger")
    depart = param.get("PortsEnFrance")
    date = param.get("date")
    print(date[7:9])
    i = 0 
    data = data.get('data')
    if data is None:
        return {}
    bato = param.get("Ferry").upper()
    print(bato)      
    ship = data[i].get('ship_name')
    dateD = data[i].get('departure').get('datetime')
  
    while (ship != bato ): 
        i = i+1
        ship = data[i].get('ship_name')
        dateD = data[i].get('departure').get('datetime')
        speech = " Le "+ship+" prend la mer à "+depart+" pour "+desti+" le "+dateD[8:10]+"/"+dateD[5:7]+" à "+dateD[11:16]+"h "
        print(speech)
        if ( dateD[8:10] != date[7:9] ):
            ship = data[0].get('ship_name')
            dateD = data[0].get('departure').get('datetime')
            speech = "A cette date("+dateD[8:10]+"/"+dateD[5:7]+") c'est "+ship+" qui prend la mer à "+depart+" pour "+desti+" à "+dateD[11:16]+"h" 
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
                  "uri": "https://www.brittany-ferries.fr/510?AccountNo=&ferry=ferryonly&journeyType=One+Way&journeyTypeState=One+Way&FCONsubmission=true&frmOGroup=9&frmORoute=&frmODay="+dateD[8:10]+"&frmOMonthYear=&frmOMonth="+dateD[5:7]+"&frmOYear="+dateD[0:4]+"&frmOMonthYearRestore=&frmODayRestore=&frmIRoute=&frmIMonth=&frmIYear=&frmIMonthYearRestore=&frmIDayRestore=&submit=Je+r%C3%A9serve "
                }
              }
             ]
            }
        else :
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
                  "uri": "https://www.brittany-ferries.fr/510?AccountNo=&ferry=ferryonly&journeyType=One+Way&journeyTypeState=One+Way&FCONsubmission=true&frmOGroup=9&frmORoute=&frmODay="+dateD[8:10]+"&frmOMonthYear=&frmOMonth="+dateD[5:7]+"&frmOYear="+dateD[0:4]+"&frmOMonthYearRestore=&frmODayRestore=&frmIRoute=&frmIMonth=&frmIYear=&frmIMonthYearRestore=&frmIDayRestore=&submit=Je+r%C3%A9serve "
                }
              }
             ]
            }
            
def makeWebhookQuartier(data):
    
    
    data = data.get('data')
    if data is None:
        return {}
    i = 0
    items = []
    print("avant while")
    while ( i < len(data) ):
	    tab ={}
	    tab["info"] = {}
	    tab.get("info")["key"] = "J'ai choisis : "+data[i].get('name')
	    tab["title"]= data[i].get('name')
	    tab["description"] = data[i].get('headline')
	    tab["image"] = {}
	    tab.get("image")["imageUri"] = data[i].get('banner').get('uri')
	    items.append(tab)
	    i += 1
		
   # print(items)
    print(tab)	

    speech = " les hotels de ce quartier sont : "
    print(speech)
    
    return {
	"fulfillmentText": speech,
	"fulfillmentMessages": 
	 [
		{
		     "platform": "ACTIONS_ON_GOOGLE",
		     "carouselSelect": 
		      {
			 "items": items
		      }   
		}
	 ]
    }
            
def makeWebhookHotel(data):
    
    
    data = data.get('data')
    if data is None:
        return {}
    name = data[0].get('name') 
    print(name)
    prix = data[0].get('starting_price').get('amount')
    print(prix)
    ImageUri = data[0].get('images')[0].get('uri')
    print(ImageUri)
    return {
	"fulfillmentMessages": 
	 [
		{
		     "platform": "ACTIONS_ON_GOOGLE",
		     "basicCard": 
		      {
			 "title": name,
			 "formattedText": "Premier prix de la chambre : "+str(prix)+"euros",
			 "image": {
			   "imageUri": ImageUri,
		           "accessibilityText": name
          		},
			 "buttons":[
				    {
				      "title": "+ D'infos",
				      "openUriAction": {
					"uri": "hbttp://stage.ngpb.io/hotel/00_32784"
				      }
				    }
				   ]
		      }   
		}
	 ]
    }           
    
    
def makeWebhookService(data,req):
	
    print("dans webhook")
    data = data.get('data')
    if data is None:
        return {}
    TabServices = data[0].get('facilityGroups')
    print(TabServices)
    result = req.get("queryResult")
    LeService = result.get("parameters").get("ServicesHotels")
    print(LeService)
    i = 0 
    j = 0	
    while ( i < len(TabServices) ):
        print("i ="+str(i))
        while ( j < len(TabServices[i].get('facilities'))):
                print("j ="+str(j))
                if (TabServices[i].get('facilities')[j] == LeService ):
                        return {
                            "fulfillmentText": "L'hotel possède bien le service : "+LeService
			 }
                j+=1
        i+=1
    return {
	"fulfillmentText": "Le service n'est pas pris en charge par l'hotel" 
	}
	
	       




def CodePort(por):
    choices = {"Le Havre":"FRLEH","Portsmouth":"GBPME","Bilbao":"ESBIO","Plymouth":"GBPLY","Cork":"IEORK","Roscoff":"FRROS","Poole":"GBPOO","Cherbourg":"FRCER","St Malo":"FRSML","Ouistrham":"FROUI","Santander":"ESSDR"}
    result = choices.get(por, '')
    return result

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

app.run(debug=False, port=port, host='0.0.0.0')
