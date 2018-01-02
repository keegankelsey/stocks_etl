USE stocks;
DROP TABLE stock_eod;
CREATE TABLE stock_eod (
	id INT NOT NULL AUTO_INCREMENT,
	symbol varchar(255) NOT NULL,
	trade_date Date,
	open DECIMAL(20,2),
	high DECIMAL(20,2),
	low DECIMAL(20,2),
	close DECIMAL(20,2),
	adjusted_close DECIMAL(20,2),
	volume DECIMAL(20,0),
	dividend_amount DECIMAL(20,2),
	split_coefficient DECIMAL(20,2),
	time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
);
