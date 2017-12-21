USE stocks;
DROP TABLE stock_eod;
CREATE TABLE stock_edo (
	id              	MEDIUMINT NOT NULL AUTO_INCREMENT,		
	symbol         		varchar(255) NOT NULL,
	trade_date	   		Date NOT NULL,
	open           		DECIMAL(20,2) NOT NULL,
	high           		DECIMAL(20,2) NOT NULL,
	low            		DECIMAL(20,2) NOT NULL,
	close           	DECIMAL(20,2) NOT NULL,
	adjusted_close		DECIMAL(20,2) NOT NULL,
	volume          	DECIMAL(20,2) NOT NULL,
	divident_amount 	DECIMAL(20,2) NOT NULL,
	split_coefficient	DECIMAL(20,2) NOT NULL,
	time_created 		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
);
