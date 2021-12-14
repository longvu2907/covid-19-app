import requests
from bs4 import BeautifulSoup
from datetime import datetime

def getAPIData():
  #get country data
  data = {}
  response = requests.get('https://coronavirus-19-api.herokuapp.com/countries').json()
  for country in response:
    name = country['country']
    data[name] = {
      "cases" : country['cases'],
      "active" : country['active'],
      "recovered" : country['recovered'],
      "deaths" : country['deaths'],
      "provinces": {}
    }

  #get vietnam province data
  req = requests.get("https://vi.wikipedia.org/wiki/Th%E1%BA%A3o_lu%E1%BA%ADn_B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam")
  soup = BeautifulSoup(req.text, 'html.parser')
  provinceData = {}
  table = soup.find("table", "wikitable")
  trs = table.find_all("tr")
  i = 0
  for tr in trs:
    if i > 1 and i < 65:
      name = tr.find_all('td')[0].text.strip()
      provinceData[name] = {
        "cases" : int(tr.find_all('td')[1].text.strip().replace('.', '')),
        "active" : int(tr.find_all('td')[2].text.strip().replace('.', '')),
        "recovered" : int(tr.find_all('td')[3].text.strip().replace('.', '')),
        "deaths" : int(tr.find_all('td')[4].text.strip().replace('.', '')),
      }
    i += 1
  data['Vietnam']['provinces'] = provinceData

  #get current datetime
  now = datetime.now()
  data['last updated'] = now.strftime("%d/%m/%Y %H:%M:%S")

  return data
