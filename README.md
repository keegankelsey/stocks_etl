# stocks_etl
Purpose: For extracting, transforming and loading stock data.

-----------
-----------

## 1. src/generate_stock_symbol_lists.py

There are now several APIs that return summary stock data. *However*, most financial API services do not simply list all serviced stocks, and if you don't know the stock symbol, it is difficult to know where to look for data. This poses a problem if you want to perform a global analysis of trading data, or mine data for hidden relationships. To circumvent this problem, we use [www.nasdaq.com](http://www.nasdaq.com/) to access full lists of stock symbols from three exchanges; NASDAQ, AMEX and NYSE. The returned list, stock symbols from more than 6,000 companies, may then be used as input to downstream API calls for collecting historical or real-time quotes.

***Example 1:*** Extract sorted list of stock symbols from NASDAQ, AMEX and NYSE.
```
$ python generate_stock_symbol_list.py
```

-----------

## 2. src/api_alphavantage_extract.py

Now that we have a list of symbols from over 6,000 companies, we can iterate over this list and use indiviaul symbols as source material for an API call. This is a script that uses the Alpha Vantage API and will return summary or intraday trading data. Documentation for underlying source data and obtaining an API key (required) may be found at [www.alphavantage.co](https://www.alphavantage.co/).

The script currently supports two functions supplied by Alpha Vantage: 1) a function that returns intraday stock quotes and, 2) a function that returns end-of-day (EOD) summary data.

`symbols.txt` is located in the data directory and contains four stock symbols (AAPL, AMZN, GOOG and TWTR) for the purpose of testing. Alpha Vantage supports API calls to a single stock at a time. For API call limitations, see Alpha Vantage documentation.


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

Data returned from Alpha Vantage comes in two forms; A) the last 100 data intervals, or B) all historical data. We don't always want a large chunk of data and, in some cases, simply want the most recent day of data. This is a script that extracts desired dates from `api_alphavantage_extract.py` output and allows you to specify your desired date range. Two functions (intraday and daily) are supported. This script also restructures the data to supply one JSON object per stock symbol and time period. 

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

Once the DB is setup, you'll want to create structure within your DB instance to house the data. Here, I've created a database within MySQL called, "stocks." The below code is SQL may be run within the MySQL command line client:
```
mysql> CREATE DATABASE stocks;
```

Now, we can create a table within stocks to begin loading all of our new data. This SQL may be run from within the MySQL command line client, or, if you have set up a "configure" file with appropriate credentials, you may simply run the SQL from command line as such:
```
$ mysql < create_tb_stock_eod.sql
```

-----------

## 5. src/load_stock_eod.sql

Finally, now that we have our data and somewhere to put our data, we need to load data into the database. MySQL can easily load data from a .csv file, so let's convert our data to a flat file. Again, we have options for how to do this. One option is to simply create another function in Python to translate JSON to the flat, csv structure. However, it is just as easy to process JSON with [jq](https://stedolan.github.io/jq/) from command-line (here, I am running Linux). I am simply printing out the full file using `cat` and then piping the output with , `|`, to `jq` for further manipulation.

```
$ cat ../data/quotes_today.json | jq -r '[.symbol, .trade_date, .open, .high, .low, .close, .adjusted_close, .volume, .dividend_amount, .split_coefficient] | @csv' > ../data/quotes_load.csv
```

Next, we can load our `../data/quotes_load.csv` file using SQL. 
```
$ mysql < load_stock_eod.sql
```

And that is it! We now have data in our database that is easy to query and access. Enjoy!
```
mysql> select * from stocks.stock_eod;
+----+--------+------------+---------+---------+---------+---------+----------------+-------------+-----------------+-------------------+---------------------+
| id | symbol | trade_date | open    | high    | low     | close   | adjusted_close | volume      | dividend_amount | split_coefficient | time_created        |
+----+--------+------------+---------+---------+---------+---------+----------------+-------------+-----------------+-------------------+---------------------+
|  1 | AAPL   | 2017-12-18 |  174.88 |  177.20 |  174.86 |  176.42 |         176.42 | 28831533.00 |            0.00 |              1.00 | 2017-12-24 06:22:37 |
|  2 | AMZN   | 2017-12-18 | 1187.37 | 1194.78 | 1180.91 | 1190.58 |        1190.58 |  2767271.00 |            0.00 |              1.00 | 2017-12-24 06:22:37 |
|  3 | GOOG   | 2017-12-18 | 1066.08 | 1078.49 | 1062.00 | 1077.14 |        1077.14 |  1552016.00 |            0.00 |              1.00 | 2017-12-24 06:22:37 |
|  4 | TWTR   | 2017-12-18 |   23.24 |   24.74 |   23.13 |   24.68 |          24.68 | 48506629.00 |            0.00 |              1.00 | 2017-12-24 06:22:37 |
+----+--------+------------+---------+---------+---------+---------+----------------+-------------+-----------------+-------------------+---------------------+
4 rows in set (0.00 sec)
```

-----------
