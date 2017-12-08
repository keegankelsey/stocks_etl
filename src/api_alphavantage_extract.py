import requests
from sys import argv
import sys
import json
import argparse

# Define and parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('call_function',
    choices=['time_series_intraday','time_series_daily_adjusted'],
    type=str,
    help='Two functions are currently supported. Intraday returns within day trade data, daily returns EOD data.')
parser.add_argument('outputsize',
    choices = ['full', 'compact'],
    type = str,
    help = 'Output size from api call. Compact restricts to last 100 data points.')
parser.add_argument('symbol_list',
    type = str,
    help = 'File with containing stock symbols. One symbol per line.')
parser.add_argument('apikey_file',
    type = str,
    help = 'File path for api key.')
parser.add_argument('-i', '--interval',
    type = str,
    default = '1min',
    choices = ['1min', '5min', '15min', '30min', '60min'],
    help = 'Optional argument specifying frequency of data for time_series_intraday. Defaults to 1min.')
args = parser.parse_args()

# Begin functions to extract and print stock symbol data
def read_apikey(apikey_file):
    """ Read in file with api key and return key. """
    try:
        with open(apikey_file) as f:
            data = f.read().replace('\n', '')
        return(data)
    except:
        print('Could not read api key')
        sys.exit('Bye')

def read_symbols(symbols):
    """ Read in file with symbols, where the file contains 
        one, and only one symbol per line. """
    try:
        with open(symbols) as f:
    	    lines = f.read().splitlines()
        return(lines)
    except:
        print('Could not read list of symbols')
        sys.exit('Bye')

def generate_url_payload(call_function, symbol, outputsize, apikey):
    """ Here, we define variables for a 'get' request. Note, 
        the api allows for various intervals (1min vs. 5min, etc.)
        when using the TIME_SERIES_INTRADAY function. For
        documentation further documentation, visit
        https://www.alphavantage.co/ """
    payload = {'symbol': symbol,
        'outputsize': outputsize,
        'datatype': 'json',
        'apikey': apikey}
    if call_function == 'time_series_daily_adjusted':
        payload['function'] = 'TIME_SERIES_DAILY_ADJUSTED'
    elif call_function == 'time_series_intraday':
        payload['function'] = 'TIME_SERIES_INTRADAY'
        payload['interval'] = args.interval
    else:
        print('Could not generate payload')
        sys.exit('Bye')
    return(payload)

def get_stock_data(payload):
    """ This function takes in a payload for an individual
        symbol, applies the payload to a 'get' request, and
        then outputs data from the api call."""
    r = requests.get('https://www.alphavantage.co/query', params = payload, timeout = 100)
    return(r.json())

def iterate_across_symbol_list(symbol_list, call_function, outputsize, apikey):
    for symbol in symbol_list:
        payload = generate_url_payload(call_function, symbol, outputsize, apikey)
        d = get_stock_data(payload)
        print(json.dumps(d))

# Run functions
# First, read in api key (provided by Alpha Vantage at https://www.alphavantage.co/)
apikey = read_apikey(args.apikey_file)

# Next, read in the list of stock symbols
symbol_list = read_symbols(args.symbol_list)

# Finally, iterate over all symbols and return data
iterate_across_symbol_list(symbol_list, args.call_function, args.outputsize, apikey)
