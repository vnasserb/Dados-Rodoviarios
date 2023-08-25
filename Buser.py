import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getText(text):
  return text.replace("\n","").strip()

def findBusesBuser(slugOrigin, slugDestination, departureDay, departureMonth, departureYear, return_date_as_string = True, date_format = '%d/%m/%Y'):
  html = urlopen("https://www.buser.com.br/onibus/"+ slugOrigin +"/"+ slugDestination +"?ida=" + str(departureYear) + "-" + str(departureMonth) + "-" + str(departureDay))
  bs = BeautifulSoup(html, 'html.parser')
  busesList = bs.find_all('div', {'class': 'gci-header'})
  keys = ['goingDay', 'arrivalDay', 'goingTime', 'arrivalTime', 'goingAdress', 'arrivalAdress', 'price', 'seat']
  dictArray = []
  stringToDate = lambda x: datetime.strptime(x, date_format)

  for bus in range(len(busesList)):
    try:
      goingDayStr, arrivalDayStr = list(map(lambda x: x.text.replace("\n","").strip() + "/" + str(departureYear), busesList[bus].find_all('p', {'class': 'ird-dia'})))
    except:
      goingDayStr, arrivalDayStr = list(map(lambda x: x.text.replace("\n","").strip() + "/" + str(departureYear), 2 * busesList[bus].find_all('p', {'class': 'ird-dia'})))

    if return_date_as_string:
      goingDay, arrivalDay = goingDayStr, arrivalDayStr
    else:
      goingDay, arrivalDay = stringToDate(goingDayStr), stringToDate(arrivalDayStr)

    goingTime, arrivalTime = list(map(lambda x: x.text.replace("\n","").strip(), busesList[bus].find_all('p', {'class': 'ird-hora'})))
    goingAdress = getText(busesList[bus].find('div', {'class': 'ir-endereco is-origem'}).text).replace("Embarque:","").strip()
    arrivalAdress = getText(busesList[bus].find('div', {'class': 'ir-endereco is-destino'}).text).replace("Desembarque:","").strip()
    price = float(getText(busesList[bus].find('div', {'class': 'preco'}).text)[3:].replace(",","."))
    seat = getText(busesList[bus].find('div', {'class': 'p-assento'}).text)
    # seatsQty = int(getText(busesList[bus].find('span', {'class': 'aviso-vagas-restantes'}).text)[:2].strip())

    dictionary = dict(zip(keys, [goingDay, arrivalDay, goingTime, arrivalTime, goingAdress, arrivalAdress, price, seat]))
    dictArray.append(dictionary)

  return pd.DataFrame(dictArray)
