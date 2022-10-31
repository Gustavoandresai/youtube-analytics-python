from youtubesearchpython import *
import json
from helper import process_results
import pandas as pd
import sys

df = pd.read_csv('youtubedataai.csv')

#search = 'ai'
#number_results = 100

#Get data and create a data frame
def get_data(search, number_results):
    data = process_results(search, number_results)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.to_csv('test.csv', index=False)

 
#with open('export.json', 'w') as f:
#    json.dump(data, f)
if __name__ == '__main__':
    get_data('cryto', 10)