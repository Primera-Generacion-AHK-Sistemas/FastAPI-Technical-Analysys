import pandas_ta as ta
import utils.ohlc_values as ohlc


def get_stoch_values(inputs):
    stoch_values = ta.stoch(inputs['high'], inputs['low'], inputs['close'])


    resp_array = []

    slowk_dict = {}
    slowk_dict['name'] = "slowk"
    slowk_dict['data'] = stoch_values['STOCHk_14_3_3'].dropna().round(2).values.tolist()
    resp_array.append(slowk_dict)

    slowd_dict = {}
    slowd_dict['name'] = "slowd"
    slowd_dict['data'] = stoch_values['STOCHd_14_3_3'].dropna().round(2).values.tolist()
    resp_array.append(slowd_dict)

    return resp_array


def get_adx_values(inputs):
    adx_values = ta.adx(inputs['high'], inputs['low'], inputs['close'])
    """
    array 
        dict
            name name
            array values
    """
    resp_array = []

    adx_dict = {}
    adx_dict['name'] = "adx"
    adx_dict['data'] = adx_values['ADX_14'].dropna().round(2).values.tolist()
    resp_array.append(adx_dict)

    di_minus_dict = {}
    di_minus_dict['name'] = "di_minus"
    di_minus_dict['data'] = adx_values['DMN_14'].dropna().round(2).values.tolist()
    resp_array.append(di_minus_dict)

    di_plus_dict = {}
    di_plus_dict['name'] = "di_plus"
    di_plus_dict['data'] = adx_values['DMP_14'].dropna().round(2).values.tolist()
    resp_array.append(di_plus_dict)

    return resp_array


def get_bbands_values(inputs):
    bbands_values = ta.bbands(inputs['close'], length=20, std=2, mamode='SMA', offset=0)


    """
    array 
        dict
            name name
            array values
    """
    resp_array = []

    upper_dict = {}
    upper_dict['name'] = "upper"
    upper_dict['data'] = bbands_values['BBU_20_2.0'].dropna().round(2).values.tolist()
    resp_array.append(upper_dict)


    mid_dict = {}
    mid_dict['name'] = "mid"
    mid_dict['data'] = bbands_values['BBM_20_2.0'].dropna().round(2).values.tolist()
    resp_array.append(mid_dict)


    lower_dict = {}
    lower_dict['name'] = "lower"
    lower_dict['data'] = bbands_values['BBL_20_2.0'].dropna().round(2).values.tolist()
    resp_array.append(lower_dict)


    ret_dict = {}
    ret_dict['name'] = "price"
    ret_dict['data'] = inputs['close'].values.tolist()
    resp_array.append(ret_dict)



    return resp_array


def get_atx_values(inputs):
    
    """
    array 
        dict
            name name
            array values
    """
    resp_array = []

    ret_dict = {}
    ret_dict['name'] = "price"
    ret_dict['data'] = inputs['close'].values.tolist()
    resp_array.append(ret_dict)

    return resp_array
    
def get_indicator_values(ticker, indicator, start_date, end_date):

    inputs, str_dates = ohlc.get_ohlc_values(ticker, start_date, end_date)

    switcher = {
        'stoch': get_stoch_values(inputs),
        'adx': get_adx_values(inputs),
        'bbands': get_bbands_values(inputs),
        'atx': get_atx_values(inputs)
    }

    indicator_values = switcher.get(indicator, "Invalid Indicator")

    return indicator_values, str_dates


def get_simple_ta(ticker):
    inputs, str_dates = ohlc.get_ohlc_days_ago(ticker, 365)

    stoch = get_stoch_values(inputs)
    adx = get_adx_values(inputs)
    bbands = get_bbands_values(inputs)

    stoch_simple_ta = get_stoch_simple_ta(stoch)
    adx_simple_ta = get_adx_simple_ta(adx)
    bbands_simple_ta = get_bbands_simple_ta(bbands, inputs)

    simple_ta = {}
    simple_ta['stoch'] = stoch_simple_ta
    simple_ta['adx'] = adx_simple_ta
    simple_ta['bbands'] = bbands_simple_ta

    return simple_ta


def get_bbands_simple_ta(bbands, inputs):
    bbands['lower'] = bbands['lower'][-1:][0]
    bbands['mid'] = bbands['mid'][-1:][0]
    bbands['upper'] = bbands['upper'][-1:][0]
    bbands['close'] = inputs['close'].round(2).values.tolist()[-1:][0]

    bbands['signal'] = 0

    if bbands['close'] > bbands['upper']:
        bbands['signal'] = 1
    elif bbands['close'] < bbands['lower']:
        bbands['signal'] = -1

    return bbands


def get_adx_simple_ta(adx):
    adx['adx'] = adx['adx'][-1:][0]
    adx['di_minus'] = adx['di_minus'][-1:][0]
    adx['di_plus'] = adx['di_plus'][-1:][0]

    adx['signal'] = 0

    if adx['adx'] > 25:
        if adx['di_minus'] > adx['di_plus']:
            adx['signal'] = -1
        elif adx['di_plus'] > adx['di_minus']:
            adx['signal'] = 1

    return adx


def get_stoch_simple_ta(stoch):
    stoch['slowk'] = stoch['slowk'][-1:][0]
    stoch['slowd'] = stoch['slowd'][-1:][0]
    stoch['signal'] = 0

    if stoch['slowk'] > 80 and stoch['slowd'] > 80:
        stoch['signal'] = -1
    elif stoch['slowk'] < 20 and stoch['slowd'] < 20:
        stoch['signal'] = 1
    
    return stoch
