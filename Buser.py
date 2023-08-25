import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getText(text):
  return text.replace("\n","").strip()

def findBusesBuser(slugOrigin, slugDestination, departureDay, departureMonth, departureYear, return_date_as_string = True):
  html = urlopen("https://www.buser.com.br/onibus/"+ slugOrigin +"/"+ slugDestination +"?ida=" + str(departureYear) + "-" + str(departureMonth) + "-" + str(departureDay))
  bs = BeautifulSoup(html, 'html.parser')
  busesList = bs.find_all('div', {'class': 'gci-header'})

  keysDatetime = ['departureDatetime', 'arrivalDatetime', 'departureStation', 'arrivalStation', 'durationTime', 'serviceClass', 'price', 'company']
  keysString = ['departureDay', 'arrivalDay', 'departureTime', 'arrivalStation', 'departureStation', 'arrivalAdress', 'durationTime', 'serviceClass', 'price', 'company']
  stringToDate = lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
  
  dictArray = []
  
  for bus in range(len(busesList)):
    try:
      departureDayStr, arrivalDayStr = list(map(lambda x: x.text.replace("\n","").strip() + "/" + str(departureYear), busesList[bus].find_all('p', {'class': 'ird-dia'})))
    except:
      departureDayStr, arrivalDayStr = list(map(lambda x: x.text.replace("\n","").strip() + "/" + str(departureYear), 2 * busesList[bus].find_all('p', {'class': 'ird-dia'})))

    departureTime, arrivalTime = list(map(lambda x: x.text.replace("\n","").strip(), busesList[bus].find_all('p', {'class': 'ird-hora'})))

    departureDatetime, arrivalDatetime = stringToDate(departureDayStr + " " + departureTime + ":00"), stringToDate(arrivalDayStr + " " + arrivalTime + ":00")

    totalDuration = arrivalDatetime - departureDatetime
    totalDurationMinutes = totalDuration.total_seconds() / 60
    durationHours = totalDurationMinutes // 60
    durationMinutes = totalDurationMinutes - durationHours * 60

    if durationMinutes > 0:
      duration = str(int(durationHours)) + "h " + str(int(durationMinutes)) + "m"
    else:
      duration = str(int(durationHours)) + "h"

    departureAdress = getText(busesList[bus].find('div', {'class': 'ir-endereco is-origem'}).text).replace("Embarque:","").strip()
    arrivalAdress = getText(busesList[bus].find('div', {'class': 'ir-endereco is-destino'}).text).replace("Desembarque:","").strip()
    price = float(getText(busesList[bus].find('div', {'class': 'preco'}).text)[3:].replace(",","."))
    seat = getText(busesList[bus].find('div', {'class': 'p-assento'}).text)
    # seatsQty = int(getText(busesList[bus].find('span', {'class': 'aviso-vagas-restantes'}).text)[:2].strip())

    if return_date_as_string:
      dictionary = dict(zip(keysString, [departureDayStr, arrivalDayStr, departureTime, arrivalTime, departureAdress, arrivalAdress, duration, seat, price, 'Buser']))
    else:
      dictionary = dict(zip(keysDatetime, [departureDatetime, arrivalDatetime, departureAdress, arrivalAdress, duration, seat, price, 'Buser']))

    dictArray.append(dictionary)

  return dictArray
