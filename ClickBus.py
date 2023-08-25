from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import time

def findBusesClickbus(slugOrigin, slugDestination, departureDay, departureMonth, departureYear, return_date_as_string = True):

  html = urlopen("https://hurb.clickbus.com.br/onibus/"+ slugOrigin +"/"+ slugDestination +"?departureDate=" + str(departureYear) + "-" + str(departureMonth) + "-" + str(departureDay))
  bs = BeautifulSoup(html, 'html.parser')
  busesList = bs.find_all("div", {'class': 'search-item search-item-direct'})
  keys = ['departureDate', 'departureTime','arrivalDate', 'arrivalTime', 'departureStation', 'arrivalStation', 'durationTime', 'serviceClass', 'price']
  dictArray = []
  stringToDate = lambda x: datetime.strptime(x, '%Y-%m-%d  %H:%M:%S')

  for bus in range(len(busesList)):

    company = bs.find_all("div", {'class': 'company'})[0]['content']
    jsonData = json.loads(busesList[bus]['data-content'].strip())

    trips = {k:v for k,v in jsonData['trips'][0].items() if k in keys}
    trips['company'] = company
    trips['price'] = float( trips['price'][2:].replace(",",".") )

    if not return_date_as_string:
      trips['departureDatetime'] = stringToDate(trips['departureDate'] + " " + trips['departureTime'] + ":00")
      trips['arrivalDatetime'] = stringToDate(trips['arrivalDate'] + " " + trips['arrivalTime'] + ":00")
      del trips['departureTime']
      del trips['arrivalTime']
      del trips['departureDate']
      del trips['arrivalDate']

    dictArray.append(trips)

  return dictArray
