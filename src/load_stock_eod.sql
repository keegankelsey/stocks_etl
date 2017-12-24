LOAD DATA LOCAL INFILE '../data/quotes_load.csv' 
INTO TABLE stocks.stock_eod
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(symbol, trade_date, open, high, low, close, adjusted_close, volume, dividend_amount, split_coefficient);
