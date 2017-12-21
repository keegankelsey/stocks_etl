# utils_stocks
Purpose: For extracting and processing stock data.

-----------
-----------

## 1. src/generate_stock_symbol_lists.py

There are now several APIs that return summary stock data, *if* you happen to know the stock symbol. However, most financial API services do not simply list all serviced stocks, and if you don't know the stock symbol it is difficult to know where to look for data. This poses a problem if you want to perform a global analysis of trading data, or mine data for hidden relationships. To circumvent this problem, we use [www.nasdaq.com](http://www.nasdaq.com/) to access full lists of stock symbols from three exchanges; NASDAQ, AMEX and NYSE. The returned list, stock symbols from more than 6,000 companies, may then be used as input to downstream API calls for collecting historical or real-time quotes.

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

## 4. src/create_tb_stock_eod.sql

We now have stock data in JSON format and can access it using various different methods. One method is to use AWS, store the JSON data in a S3 bucket and then perform a serverless query using [Athena](https://aws.amazon.com/athena/). Another method, is to load the data into a more traditional database such as MySQL, PostgreSQL or Oracle. There are pros and cons to all methods, however let's use MySQL to store and access our data.

I've already created a MySQL database (DB) instance in my AWS account using RDS. Alternatively, MySQL may be set up and run on your local computer.

Once the DB is setup, you'll want to create structure within your instance. Here, I've created a database within MySQL called, "stocks." The below code is SQL may be run within the MySQL command line client:
```sql
CREATE DATABASE stocks;
```


