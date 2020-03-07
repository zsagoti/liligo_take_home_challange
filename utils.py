import pandas as pd
import numpy as np
import os

def load_listings(listings_urls):
    if not os.path.exists('raw_data'):
        os.mkdir('raw_data')
    listings_data={}
    for location in listings_urls:
        raw_file="raw_data/listings_" + location + ".gz"
        if not os.path.exists(raw_file):
            print('Downloading ' + location + ' data...')
            r = requests.get(listings_urls[location], allow_redirects=True)
            open(raw_file, 'wb').write(r.content)
            print('Done.')
        else:
            print(location + " data has already downloaded.")
        listings_data[location] = pd.read_csv(raw_file)
    return pd.concat(listings_data,names=['location']).droplevel(1)
