import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        listings_data[location] = pd.read_csv(raw_file, dtype={'neighbourhood':'str',
                                                               'zipcode':'str',
                                                               'weekly_price':'str',
                                                               'monthly_price':'str',
                                                               'license':'str'})
    return pd.concat(listings_data,names=['location']).droplevel(1)
    
def my_plot_pie(data, title='',suptitle=''):
    labels = data.index
    sizes = data.values
    explode = len(labels)*[0.01]
    plt.pie(sizes, explode=explode, labels=labels,# colors=colors,
    autopct='%1.1f%%', shadow=False, startangle=90)
    plt.title(title)
    plt.suptitle(suptitle)                 
    plt.axis('equal')
    plt.show()
