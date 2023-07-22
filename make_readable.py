import sys
import pandas as pd
import properties
import locations
import scraper

from datetime import datetime
from bidict import ON_DUP_DROP_OLD

if len(sys.argv) != 2:
    print("Exiting...  provide filename!")
    exit()

filename = sys.argv[1]
clsname = filename.split('/')[0]
cls = eval(f'scraper.{clsname}.properties')

df = pd.read_csv(filename)

for column in df.columns:
    df[column] = df[column].apply(cls.inverseGet, key=column)

df['location'] = df['location'].apply(locations.getLocationName)

new_filename = filename.split('.')[0] + f'{datetime.now().date()}.csv'

df.to_csv(new_filename,index=False)