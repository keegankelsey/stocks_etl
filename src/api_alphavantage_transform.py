from sys import argv
import sys
import json
import argparse
from datetime import datetime, timedelta
from pytz import timezone
import pytz


# Specify default start and end dates using Eastern TZ
utc = pytz.utc
eastern = timezone('US/Eastern')
now = datetime.now(tz=utc)
now_date = now.astimezone(eastern).strftime('%Y-%m-%d')

# Define and parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('stock_quotes',
    type=str,
    help='Output from api_alphavantage.py')
parser.add_argument('-sd', '--start_date',
    type = str,
    default = now_date,
    help = 'Desired start date. For example, "2017-12-07." Default is current date (Eastern time zone).')
parser.add_argument('-ed', '--end_date',
    type = str,
    default = now_date,
    help = 'Desired end date. For example, "2017-12-11." Default is current date (Eastern time zone).')
args = parser.parse_args()

# Raise error if start_date is after end_date
if args.start_date > args.end_date:
    print('start_date, {}, must be earlier than or equal to end_date, {}.'.format(args.start_date, args.end_date))
    sys.exit('Bye')

# Begin functions to extract and print stock symbol data
def read_stock_quotes(stock_quotes, start_date, end_date):
    """ Convert output from api call to desired set
        of quote dates """

    # Approved list of functions
    function_list = ['Time Series (Daily)',
        'Time Series (1min)',
        'Time Series (5min)',
        'Time Series (15min)',
        'Time Series (30min)',
        'Time Series (60min)']
    
    with open(args.stock_quotes, 'r') as f:
        for line in f:
            x = json.loads(line)
            symbol = x['Meta Data']['2. Symbol']
            quote_key = list(x)[1]
            if quote_key == function_list[0]:
                for date_time in list(x[quote_key]):
                    if start_date <= date_time <= end_date:
                        d = x[quote_key][date_time]
                        obj = {'symbol': symbol,
                            'trade_date': date_time,
                            'open': float(d['1. open']),
                            'high': float(d['2. high']),
                            'low': float(d['3. low']),
                            'close': float(d['4. close']),
                            'adjusted_close': float(d['5. adjusted close']),
                            'volume': float(d['6. volume']),
                            'divident_amount': float(d['7. dividend amount']),
                            'split_coefficient': float(d['8. split coefficient'])}
                        print(json.dumps(obj))
            elif quote_key in function_list[1:6]:
                for date_time in list(x[quote_key]):
                    tm = date_time.split(' ')
                    trade_date = tm[0]
                    trade_time = tm[1]
                    if start_date <= trade_date <= end_date:
                        d = x[quote_key][date_time]
                        obj = {'symbol': symbol,
                            'trade_date': trade_date,
                            'trade_time': trade_time,
                            'open': float(d['1. open']),
                            'high': float(d['2. high']),
                            'low': float(d['3. low']),
                            'close': float(d['4. close']),
                            'volume': float(d['5. volume'])}
                        print(json.dumps(obj))
            else:
                print('Data type is not supported')
                sys.exit('Bye')

# Run functions
read_stock_quotes(args.stock_quotes, args.start_date, args.end_date)
