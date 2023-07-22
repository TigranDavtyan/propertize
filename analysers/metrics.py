import json
from datetime import datetime, timedelta

import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

from sklearn.linear_model import LinearRegression

import sys
sys.path.append('../realtorbot/')
from locations import *

class BasicMetrics:
    def __init__(self, df = None):
        self.df = df
        self.median_price = None
        self.median_price_per_square = None
        self.average_days_on_market = None
        self.expected_days_to_sell = None
        self.number_of_properties = None
        self.median_monthly_mortgage_payment = None
        self.average_floor_area = None
        self.number_of_new_construction = None
        self.best_offers = None

    def to_dict(self):
        return {
            'mp'   : self.median_price,
            'mpps' : self.median_price_per_square,
            'adom' : self.average_days_on_market,
            'edts' : self.expected_days_to_sell,
            'nop'  : self.number_of_properties,
            'mmmp' : self.median_monthly_mortgage_payment,
            'afa'  : self.average_floor_area,
            'nonc' : self.number_of_new_construction,
            'bo'   : self.best_offers
        }

    def from_dict(self, dict):
        self.median_price = dict['mp']
        self.median_price_per_square = dict['mpps']
        self.average_days_on_market = dict['adom']
        self.expected_days_to_sell = dict['edts']
        self.number_of_properties = dict['nop']
        self.median_monthly_mortgage_payment = dict['mmmp']
        self.average_floor_area = dict['afa']
        self.number_of_new_construction = dict['nonc']
        self.best_offers = dict['bo']

    def __str__(self):
        r = f'''
    median_price = {self.median_price}
    median_price_per_square = {self.median_price_per_square}
    average_days_on_market = {self.average_days_on_market}
    expected_days_to_sell = {self.expected_days_to_sell}
    number_of_properties = {self.number_of_properties}
    median_monthly_mortgage_payment = {self.median_monthly_mortgage_payment}
    average_floor_area = {self.average_floor_area}
    number_of_new_construction = {self.number_of_new_construction}
    best_offers = {self.best_offers}
'''
        return  r
    
    def calculate(self):
        '''Calculate all the metrics'''

        #Median dollar price
        self.median_price = self.df['dollar_price'].median()
        
        #Median price per square
        price_per_square = self.df['dollar_price'] / self.df['floor_area']
        self.median_price_per_square = price_per_square.median()

        #Average days on market 
        df_ = self.df[self.df['closed_item'] == 0]
        self.average_days_on_market = (datetime.now() - df_['posted_date']).dt.days.mean()

        #Expected days to sell
        sold_items = self.df[self.df['closed_item'] == 1]
        sold_items_days_on_market = (sold_items['update_date'] - sold_items['posted_date']).dt.days
        self.expected_days_to_sell = sold_items_days_on_market.mean()

        #Number of properties 
        self.number_of_properties = len(self.df)

        #Median monthly mortgage payment 
        mortgage_rate = 13 # example rate
        years_to_pay = 20 # example term
        self.median_monthly_mortgage_payment = (self.df['dollar_price'] * 0.8) * (mortgage_rate/12) * ((1+mortgage_rate/12)**(years_to_pay*12)) / ((1+mortgage_rate/12)**(years_to_pay*12) - 1)
        self.median_monthly_mortgage_payment = self.median_monthly_mortgage_payment.median()
        # self.df['mortgage_payment'] = (self.df['dollar_price'] * 0.8) * (mortgage_rate/12) * ((1+mortgage_rate/12)**(years_to_pay*12)) / ((1+mortgage_rate/12)**(years_to_pay*12) - 1)
        # self.median_monthly_mortgage_payment = self.df['mortgage_payment'].median()

        #Average floor area 
        self.average_floor_area = self.df['floor_area'].mean()

        #Number of new construction
        self.number_of_new_construction = self.df['new_construction'].sum()

        self.calculate_best_offers()

    def calculate_best_offers(self):
        origin = self.df[['new_construction', 'floors_in_the_building','elevator', 'floor_area', 'floor','number_of_bathrooms', 'number_of_rooms', 'ceiling_height', 'dollar_price']].copy(True)
        origin.dropna(inplace=True)

        if len(origin) < 10:
            return

        X = origin.drop('dollar_price', axis=1)

        y = origin['dollar_price']

        model = LinearRegression().fit(X, y)

        origin['score'] = X.dot(model.coef_)

        origin = origin.sort_values(by=['score'], ascending=False)

        best_indexes = origin.iloc[5:15].index
        scores = origin.iloc[5:15]['score']
        self.best_offers = {i:s for i,s in zip(best_indexes, scores)}

class NRoomMetrics(BasicMetrics):
    def __init__(self, df = None, nroom = None):
        self.df = df
        if  df is not None and nroom:
            self.df = df[df['number_of_rooms'] == nroom]

        super().__init__(self.df)

class NDaysMetrics(BasicMetrics):
    def __init__(self, df = None, ndays = None):
        self.df = df
        if df is not None and ndays:
            start_date = datetime.now() - timedelta(days=ndays)
            self.df = df[df['update_date'] > start_date]
        
        self.room1 = NRoomMetrics(self.df, 1)
        self.room2 = NRoomMetrics(self.df, 2)
        self.room3 = NRoomMetrics(self.df, 3)
        self.room4 = NRoomMetrics(self.df, 4)

        super().__init__(self.df)
    
    def __str__(self):
        r = f'''
    {super().__str__()}
    Rooms 1 
        {self.room1.__str__()}

    Rooms 2 
        {self.room2.__str__()}

    Rooms 3 
        {self.room3.__str__()}

    Rooms 4 
        {self.room4.__str__()}

'''
        return r

    def calculate(self):
        super().calculate()
        self.room1.calculate()
        self.room2.calculate()
        self.room3.calculate()
        self.room4.calculate()

    def to_dict(self):
        basic = super().to_dict()
        basic.update({
            'r1' : self.room1.to_dict(),
            'r2' : self.room2.to_dict(),
            'r3' : self.room3.to_dict(),
            'r4' : self.room4.to_dict()
        })
        return basic
    
    def from_dict(self, dict):
        self.room1.from_dict(dict['r1'])
        self.room2.from_dict(dict['r2'])
        self.room3.from_dict(dict['r3'])
        self.room4.from_dict(dict['r4'])
        super().from_dict(dict)

class LocationMetrics(BasicMetrics):
    def __init__(self, df = None,  location = None):
        self.df = df
        if df is not None and location:
            if type(location) == int:
                self.df = df[df['location'] == location]
            elif type(location) == LocationGroup:
                self.df = df[df['location'] in location]
            else:
                raise ValueError(f'Inapropiate argument "location" = {location}')

        self.days30 = NDaysMetrics(self.df, 30)
        self.days90 = NDaysMetrics(self.df, 90)

        super().__init__(self.df)

        return self
    
    def __str__(self):
        r = f'''{super().__str__()}

30 days {self.days30.__str__()}

90 days {self.days90.__str__()}
    
'''
        return r
    
    def to_dict(self):
        basic = super().to_dict()

        basic.update({
            'd30' : self.days30.to_dict(),
            'd90' : self.days90.to_dict()
        })

        return basic
    
    def from_dict(self, dict):
        self.days30.from_dict(dict['d30'])
        self.days90.from_dict(dict['d90'])
        super().from_dict(dict)
    
    def calculate(self):
        super().calculate()
        self.days30.calculate()
        self.days90.calculate()

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=0)

    def load(self, filename):
        with open(filename, 'r') as file:
            self.from_dict(json.load(file))
    
    def loadFile(self, file):
        self.from_dict(json.load(file))
