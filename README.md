# utils_stocks
Purpose: For extracting and processing stock data.

-----------
-----------

## 1. src/generate_stock_symbol_lists.py

There are now several APIs that return summary stock data, *if* you happen to know the stock symbol. However, if you are not interested in any particular company and want to perform a global analysis of trading data, there are few APIs that list all stocks serviced. Here, we use [www.nasdaq.com](http://www.nasdaq.com/) to access full lists of stock symbols from three exchanges; NASDAQ, AMEX and NYSE. The returned list, stock symbols from more than 6,000 companies, may then be used as input to downstream API calls.

***Example 1:*** Extract sorted list of stock symbols from NASDAQ, AMEX and NYSE.
```
$ python generate_stock_symbol_list.py
```

-----------

## 2. src/api_alphavantage_extract.py

This is a script that uses the Alpha Vantage API. Documentation for underlying source data and obtaining an API key (required) may be found at [www.alphavantage.co](https://www.alphavantage.co/).

The script currently supports two functions supplied by Alpha Vantage: 1) a function that returns intraday stock quotes and, 2) a function that returns end-of-day (EOD) summary data.

`symbols.txt` is located in the data directory and contains four stock symbols (AAPL, AMZN, GOOG and TWTR) for the purpose of testing.


***Example 1:*** Extract the last 100 time points from stocks, based on 5 minute intervals.
```
$ python api_alphavantage_extract.py time_series_intraday compact ../data/symbols.txt ~/.api/api_alphavantage.key -i 5min 
```

***Example 2:*** Extract all daily historical summary data (open, high, low, close, etc.) from four stocks.
```
$ python api_alphavantage_extract.py time_series_daily_adjusted full ../data/symbols.txt ~/.api/api_alphavantage.key
```

-----------

## 3. src/api_alphavantage_transform.py

This is a script that extracts desired dates from api_alphavantage_extract.py output. Two functions (intraday and daily) are supported. This script also restructures the data to supply one JSON object per stock symbol and time period.

`quotes_intraday.json` and `quotes_daily.json` are located in the data directory and are supplied for the purpose of testing.


***Example 1:*** Extract intraday stock quotes from 2017-12-11
```
$ python api_alphavantage_transform.py ../data/quotes_intraday.json -sd 2017-12-11 -ed 2017-12-11
```

***Example 2:*** Extract EOD summary data for dates ranging from 2017-12-01 to 2017-12-05.
```
$ python api_alphavantage_transform.py ../data/quotes_daily.json -sd 2017-12-01 -ed 2017-12-05
```

-----------

