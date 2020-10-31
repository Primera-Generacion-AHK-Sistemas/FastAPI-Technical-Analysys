import utils.cedears as cedears
from datetime import datetime


# obtener el nombre del cedear buscando por ticker
def get_name(ticker):
    for i in cedears.lista:
        if(i['ticker'] == ticker):
            return i['nombre']

def getCedears():
    return cedears.lista
    
# obtener el ratio del cedear buscando por ticker
def get_ratio(ticker):
    for i in cedears.lista:
        if(i['ticker'] == ticker):
            return i['ratio']


# convertir fechas en formato epoch a YYYY/MM/DD
# devolver como lista
def date_converter(dates):
    str_dates = []
    for item in dates:
        # item = datetime.utcfromtimestamp(item/1000000000).strftime('%Y/%m/%d')
        item = item.strftime('%Y/%m/%d')
        str_dates.append(item)
    
    return str_dates


lista = {'stoch':['slowk','slowd'], 'adx':['adx','di_plus','di_minus'], 'bbands':['upper','mid','lower','price'], 'atx':['price']}

def get_indicators_types():
    return lista

def get_indicators_values():
    return lista


def ta_json_format(ticker, indicator, indicator_values, str_dates):
    ta_json = {}
    ta_json['ticker'] = ticker
    ta_json['name'] = get_name(ticker)
    ta_json['indicator'] = indicator
    ta_json['values'] = lista[indicator]
    ta_json['data']= indicator_values
    ta_json['date'] = str_dates
    return ta_json

"""
array 
    dict
        name name
        array values
"""



