import pandas as pd
import lxml
import json
import requests
from datetime import date, datetime
#-------------

def CoinDate(date):
  print(date)

  date_clock = date[11:20:]
  date_ajust = date[:10:]
  date_day = date_ajust[8:10:]
  date_year = date_ajust[:4:]
  date_month_test = date_ajust[5:7:]
  date_date = '{}/{}/{} {}'.format(date_day, date_month_test, date_year, date_clock)

  #print(date_clock)
  return date_date

def cotation_all(cotation):
  #lista = requests.get('https://economia.awesomeapi.com.br/all')
  #cotation = json.loads(lista.text)

  dollar_name = cotation['USD']['name']
  dollar = cotation['USD']['high']
  dollar = round(float(dollar),2)
  str_date = cotation['USD']['create_date']
  str_date = datetime.fromisoformat(str_date)
  dollar_date = str_date.strftime('%d/%m/%Y %H:%M:%S')

  dollar_cad_name = cotation['CAD']['name']
  dollar_cad = cotation['CAD']['high']
  dollar_cad = round(float(dollar_cad),2)
  str_date = cotation['CAD']['create_date']
  str_date = datetime.fromisoformat(str_date)
  dollar_cad_date = str_date.strftime('%d/%m/%Y %H:%M:%S')

  btc_name = cotation['BTC']['name']
  btc = cotation['BTC']['high']
  btc = round(float(btc),2)
  str_date = cotation['BTC']['create_date']
  str_date = datetime.fromisoformat(str_date)
  btc_date = str_date.strftime('%d/%m/%Y %H:%M:%S')

  euro_name = cotation['EUR']['name']
  euro = cotation['EUR']['high']
  euro = round(float(euro),2)
  str_date = cotation['EUR']['create_date']
  str_date = datetime.fromisoformat(str_date)
  euro_date = str_date.strftime('%d/%m/%Y %H:%M:%S')

  libra_name = cotation['GBP']['name']
  libra = cotation['GBP']['high']
  libra = round(float(libra),2)
  str_date = cotation['GBP']['create_date']
  str_date = datetime.fromisoformat(str_date)
  libra_date = str_date.strftime('%d/%m/%Y %H:%M:%S')

  '''
  print('#########################################')
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(dollar_name, dollar, dollar_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(dollar_cad_name, dollar_cad, dollar_cad_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(dollar_aus_name, dollar_aus, dollar_aus_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(bitcoin_name, btc, bitcoin_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(litcoin_name, ltc, litcoin_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(euro_name, euro, euro_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(libra_name, libra, libra_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(peso_name, peso, peso_date))
  print('VALOR DA COTAÇÃO - {}: {} - {}'.format(iene_name, iene, iene_date))
  print('##########################################\n')
  print('\n')
  print('                            A.M.O COTACÕES')
  '''
  #----------------------------------------------------------

  dados = [ [dollar_name, dollar, dollar_date],
            [dollar_cad_name, dollar_cad, dollar_cad_date],
            [btc_name, btc, btc_date],
            [euro_name, euro, euro_date],
            [libra_name, libra, libra_date],
          ]

  header = ['MOEDA', 'VALOR', 'DATA_COTA']

  df = pd.DataFrame(data=dados, columns=header)

  return df

def today_is(hj):

  data_em_texto = hj.strftime('%d/%m/%Y')

  dias = ('Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo')
  mes = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')

  day_week = dias[hj.weekday()]
  day = data_em_texto[:2:]
  year = data_em_texto[6:10:]
  month_test = data_em_texto[3:5:]

  month = mes[int(month_test[1]) - 1]

  dates = [day_week, day, year, month]

  return dates


def dollar_last_days(df):

  var_readed = [df['VALOR'].loc[0], str(df['DATA_COTA'].loc[0])[:10]]
  df_dolar = pd.read_excel('DB_JSON/DF_DOLAR.xlsx')

  df_dolar.drop('Unnamed: 0', axis=1, inplace=True)
  header2 = ['VALOR','DATA_COTA']
  
  df2 = pd.DataFrame(data=[var_readed], columns=header2, index=[len(df_dolar)])
  new = df_dolar.append(pd.concat([df2]))

  read = df_dolar[df_dolar['DATA_COTA'] == var_readed[1]]

  if len(read) == 0:
    new.to_excel('DB_JSON/DF_DOLAR.xlsx')


def read_dollar_grafic():
  
  df_dolar = pd.read_excel('DB_JSON/DF_DOLAR.xlsx')

  read_value, read_date = [], []
  for a in range(1, len(df_dolar['VALOR'])):
    if df_dolar['DATA_COTA'].loc[a] != '-':
      read_value.append(df_dolar['VALOR'].loc[a])
      read_date.append(df_dolar['DATA_COTA'].loc[a][:10])

  read_all = [read_value, read_date]

  return read_all