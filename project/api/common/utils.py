import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import random
import config
from ..start import abort
def price_direct_conversion(symbol, convert):
    """
        For 1 symbol we got output convert. 
        Exemple: 1 $ = 1, 27 €
                 1 BTC = 36000 $
                 1 ETH = 36000 $
                 ...
    """
    URL = config.COINMARKET_BASE_URL+"/v1/tools/price-conversion"

    API_KEYS = config.COINMARKET_API_KEYS
    
    parameters = {
    'amount':'1',
    'symbol': symbol,
    'convert': convert
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': random.choice(API_KEYS),    # get random key into api_keys
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(URL, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise Exception()

def parse_direct_conversion(data: dict):
    try:
        convert = list(data.get("data").get("quote").keys())[0]
        price = data.get("data").get("quote").get(convert).get("price")
        return price
    except Exception as e:
       abort(e.args)

def fiat_conversion(symbol, convert):
    """
        :param symbol: According to ISO 4217. Example: XOF
        :param convert: According to ISO 4217. Example: CHF
        For 1 symbol we got output convert. 
        Exemple: 1 $ = 540 XOF
                 ...    
    """
    URL = config.CURRENCY_LAYER_BASE_URL+"/live"

    API_KEYS = config.CURRENCY_LAYER_API_KEYS
    parameters = {
    'access_key': random.choice(API_KEYS),      # get random key into api_keys
    'source': symbol,
    'currencies': convert,
    'format': 1
    }
    headers = {
    'Accepts': 'application/json',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(URL, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        raise Exception()

def price_fiat_conversion(symbol, convert):
    if symbol == 'USD':
        return parse_fiat_conversion(fiat_conversion(symbol, convert))
    elif convert == 'USD':
        return 1/(parse_fiat_conversion(fiat_conversion(convert, symbol)))
    else:
        Exception
        
def parse_fiat_conversion(data: dict):
    try:
        convert = list(data.get("quotes").keys())[0]
        price = data.get("quotes").get('USDXOF')
        return price
    except Exception as e:
        abort(e.args)