# utils_stocks
A utilities repo for extracting and processing stock data.

-----------
-----------

## 1. src/api_alphavantage_extract.py

This is a python script that uses the Alpha Vantage API. Documentation and API key (required) may be obtained at [www.alphavantage.co](https://www.alphavantage.co/).

The script currently supports two functions supplied by Alpha Vantage; a function that 1) returns intraday stock quotes and a function that 2) returns end-of-day (EOD) stock quotes.

`data/symbols.txt` is supplied and contains four stock symbols (AAPL, AMZN, GOOG and TWTR) for the purpose of testing.


***Example 1:*** Extract the last 100 time points from stocks, based on 5 minute intervals.
```
python api_alphavantage_extract.py \
	time_series_intraday \
	compact \
	../data/symbols.txt \
	~/.api/api_alphavantage.key \
	-i 5min 
```

***Example 2:*** Extract all daily historical summary data (open, high, low, close, etc.) from four stocks.
```
python api_alphavantage_extract.py \
	time_series_daily_adjusted \
	full \
	../data/symbols.txt \
	~/.api/api_alphavantage.key
```

-----------
