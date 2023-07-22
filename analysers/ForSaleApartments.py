import pickle
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio
import os

import sys
sys.path.append('../realtorbot/')
from locations import *

from .metrics import *

class ForSaleApartmentsAnalyser:
    def __init__(self, df = None, updates = None):
        self.main_directory = './ForSale/Apartments/'
        if  df is not None and not df.empty:
            self.df = df
        else:
            self.df = pd.read_csv(f'{self.main_directory}listings.csv')
        
            self.df.set_index('itemid', inplace=True)

        self.df.drop(['children_are_welcome','pets_allowed','utility_payments','prepayment','type','condition','garage',
                        'exterior_finish','location_from_the_street', 'entrance','lease_type','minimum_rental_period',
                        'interior_finishing','mortgage_is_possible','handover_date'], axis=1, inplace=True)
        
        self.df['posted_date'] = pd.to_datetime(self.df['posted_date'])
        self.df['update_date'] = pd.to_datetime(self.df['update_date'])

        if updates:
            self.updates = updates
        else:
            with open(f'{self.main_directory}updates.pickle', 'rb') as file:
                self.updates = pickle.load(file)

        self.remove_duplicate_updates()
        self.filter_updates()

    def remove_duplicate_updates(self):
        for id, update in self.updates.items():
            unique_dates = set()
            unique_list = []

            for item in update:
                item[0] = datetime.combine(item[0].today(), datetime.min.time())
                date = f'{item[0].date()}_{item[1]}'
                if date not in unique_dates:
                    unique_dates.add(date)
                    unique_list.append(item)

            self.updates[id] = unique_list

    def filter_updates(self):
        for id, item in self.updates.items():
            filtered = []
            for update in item:
                if not update[0] or not update[1] or update[1] > 3000000 or update[1] < 10000 or update[0].year < 2000:
                    continue
                filtered.append([update[0],update[1]])
            self.updates[id] = filtered

    def analyse_updates_by_location(self):
        updates_for_locations = {}
        for id, update in self.updates.items():
            location = int(self.df.at[id, 'location'])
            parent_location = [parent_location for parent_location in MARZER.keys() if location in parent_location][0].ID
            if location not in updates_for_locations.keys(): updates_for_locations[location] = []
            if parent_location not in updates_for_locations.keys(): updates_for_locations[parent_location] = []
            updates_for_locations[location].extend(update)
            updates_for_locations[parent_location].extend(update)
        
        for location, updates in updates_for_locations.items():
            df = pd.DataFrame(updates, columns=['Date', 'Price'])
            df.set_index('Date', inplace=True)

            df_high_low = df.groupby(pd.Grouper(freq='D')).agg({'Price': ['min', 'max', 'median', 'mean']})
            df_high_low.columns = ['Low', 'High', 'Median', 'Mean']
            df_high_low.index = pd.to_datetime(df_high_low.index)

            fig = go.Figure(data=[go.Candlestick(x=df_high_low.index,
                                                open=df_high_low['Median'],
                                                high=df_high_low['High'],
                                                low=df_high_low['Low'],
                                                close=df_high_low['Median'],
                                                increasing_line_color='green',
                                                decreasing_line_color='red')])

            loc_name, parent_loc_name = getLocationParentLocationNames(location)
            today = datetime.now().date()

            fig.update_layout(title=f'{today} : Daily High-Low and median prices in {loc_name}' +
                               ('' if parent_loc_name == '' else f'({parent_loc_name})'),
                            yaxis_title='Price $',
                            xaxis_rangeslider_visible=False)

            directory = f'{self.main_directory}{today}/{parent_loc_name}/{loc_name}'

            os.makedirs(directory, exist_ok=True)

            pio.write_image(fig, f'{directory}/daily_high_low_median_prices.png')

            self.df = self.df[(self.df['dollar_price'] < 3000000) & (self.df['dollar_price'] > 0)]
            self.df = self.df[(self.df['floor_area'] < 1000) & (self.df['floor_area'] > 0)]
            
            metrics = LocationMetrics(self.df, location)
            metrics.calculate()
            metrics.save(f'{directory}/metrics.json')