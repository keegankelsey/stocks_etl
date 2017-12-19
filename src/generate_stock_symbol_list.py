import csv
import requests
import io
import sys

# Define urls with stock data
url_nasdaq_csv = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
url_nyse_csv = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'
url_amex_csv = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download'

# Define functions
def read_stock_flat_file(stock_csv, return_colnames=False):
    """
        Read in csv style data from nasdaq url, return dict.
    """
    try:
        r = requests.get(stock_csv)
        reader_list = csv.DictReader(io.StringIO(r.text))
    except:
        print('Could not retrieve stock data')
        sys.exit('Bye')
    if return_colnames == True:
        return(reader_list.fieldnames)
    else:
        return(reader_list)

def extract_single_data_type(reader_list, feature='Symbol'):
    """
        Read in dict and return a single data type (feature)
        from the list of dicts. 
    """
    d = []
    for row in reader_list:
        x = row[feature]
        if feature == 'Symbol':
            xm = x.replace(" ", "")
            d.append(xm)
        else:
            pass
    return(d)

def dedup_sort_print(list_of_items):
    """
        Take list of stocks, remove non-alpha symbols,
        dedup, sort and then print list
    """
    xl = [w for w in list_of_items if w.isalpha()]
    x = list(set(xl))
    x.sort()
    for item in x:
        print(item)


# Run functions
# Read in and extract NASDAQ symbol
nasdaq_dict = read_stock_flat_file(url_nasdaq_csv)
nasdaq_symb = extract_single_data_type(nasdaq_dict)
# Read in and extract NYSE symbol
nyse_dict = read_stock_flat_file(url_nyse_csv)
nyse_symb = extract_single_data_type(nyse_dict)
# Read in and extract AMEX symbol
amex_dict = read_stock_flat_file(url_amex_csv)
amex_symb = extract_single_data_type(amex_dict)

# Join, sort and dedup lists
all_symbs = nasdaq_symb + nyse_symb + amex_symb
dedup_sort_print(all_symbs)

