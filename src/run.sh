# Generate list of stock symbols
python generate_stock_symbol_list.py > ../data/stock_symbols.txt


# Extract summary data from API
python api_alphavantage_extract.py \
    time_series_daily_adjusted \
    compact \
    ../data/symbols.txt \
    ~/.api/api_alphavantage.key > ../data/quotes_daily.json

# Transform data
python api_alphavantage_transform.py \
    ../data/quotes_daily.json \
    -sd 2017-12-18 \
    -ed 2017-12-18
