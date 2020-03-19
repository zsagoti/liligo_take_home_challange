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
#    plt.show()

def format_vertical_headers(df):
    """Display a dataframe with vertical column headers"""
    styles = [dict(selector="th", props=[('width', '40px')]),
              dict(selector="th.col_heading",
                   props=[("writing-mode", "vertical-rl"),
                          ('transform', 'rotateZ(180deg)'), 
                          ('height', '150px'),
                          ('vertical-align', 'top')])]
    return (df.fillna('').style.set_table_styles(styles))

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

def calc_review_means(group, review_features):
    review_means=pd.DataFrame()
    for feat in review_features[1:]:
        review_means[feat]=group[feat]*group['number_of_reviews']
    review_means['number_of_reviews']=group['number_of_reviews']

    return review_means.sum(axis=0)/review_means['number_of_reviews'].sum()