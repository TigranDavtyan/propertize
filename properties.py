from bidict import bidict
import logging
logger = logging.getLogger('lstamscraper')


def default_func(val):
    logger.error(f'Dont have corresponding value for {val}')
    return val

class property:
    def __init__(self, dict: bidict, func = default_func):
        self.bidict = dict
        self.func = func

    def get(self, val) -> int:
        if val in self.bidict.keys():
            return self.bidict[val]
        else:
            return self.func(val)

    def inverse(self, val) -> str:
        if val in self.bidict.inverse.keys():
            return self.bidict.inverse[val]
        else:
            return val

class HouseProperties:
    default                  = property(bidict({}), default_func )
    itemid                   = property(bidict({}), lambda val: int(val))
    location                 = property(bidict({}), lambda val: int(val))
    construction_type        = property(bidict({'bricks':-2,'stone': -1, 'monolith': 0, 'panels': 1, 'cassette':2, 'wooden':3}))
    new_construction         = property(bidict({'no': -1, 'yes': 1}))
    elevator                 = property(bidict({'not_available': -1, 'available': 1}))
    balcony                  = property(bidict({'closed_balcony': -3, 'not_available': -1, 'open_balcony': 1, 'multiple_balconies': 3}))
    furniture                = property(bidict({'not_available': -3, 'available': -1, 'by_agreement': 1, 'partial_furniture': 3}))
    renovation               = property(bidict({'old_renovation': -3, 'designer_renovation': -2, 'major_renovation': -1, 'cosmetic_renovation': 0, 'no_renovation': 1, 'partial_renovation': 2, 'euro_renovation': 3}))
    children_are_welcome     = property(bidict({'negotiable': -1, 'no': 0, 'yes': 1}))
    pets_allowed             = property(bidict({'negotiable': -1, 'no': 0, 'yes': 1}))
    utility_payments         = property(bidict({'not_included': -1, 'included': 0, 'by_agreement': 1}))
    prepayment               = property(bidict({'by_agreement': -2, 'without_prepayment': -1}), lambda val : int(val.split('_')[0]) if val else None )
    type                     = property(bidict({'house': -13, 'agricultural': -11, 'retail_space': -9, 'for_residential_development': -7, 'warehouse': -5, 'industrial_and_manufacturing': -3, 'for_public_buildings': -1, 'restaurant': 1, 'garage': 3, 'multifunctional_space': 5, 'functioning_business': 7, 'for_general_purpose': 9, 'apartment': 11, 'country_house': 13, 'townhouse': 15}))
    condition                = property(bidict({'house_is_finished': -1, 'house_is_under_construction': 0, 'house_is_unfinished': 1}))
    garage                   = property(bidict({'not_available': 0}), lambda val : int(val.split('_')[0]) if val else None)
    exterior_finish          = property(bidict({'metal': 0}))
    location_from_the_street = property(bidict({'first_line': -1, 'second_line': 1}))
    entrance                 = property(bidict({'separate_from_the_street': -1, 'separate_from_the_courtyard': 0, 'common_from_the_street': 1}))
    lease_type               = property(bidict({'direct_lease': 0}))
    minimum_rental_period    = property(bidict({'1_year': 0}))
    interior_finishing       = property(bidict({'unfinished_interior': -1, 'prefinished_interior': 0, 'turnkey': 1}))
    mortgage_is_possible     = property(bidict({'yes': -1, 'no': 1}))
    handover_date            = property(bidict({}), lambda val: val) #{'q2_2023': -1.0, 'q2_2024': 0.0, 'q2_2025': 1.0}
    floor_area               = property( bidict({}),lambda val : int(val.split('_')[0].replace(',',''))  if val else None)
    floors_in_the_building   = property( bidict({}),lambda val : int(val.replace('+',''))  if val else None)
    number_of_bathrooms      = property( bidict({}),lambda val : int(val[0])  if val else None)
    number_of_rooms          = property( bidict({}),lambda val : int(val[0])  if val else None)
    ceiling_height           = property( bidict({}),lambda val : float(val.split('_')[1])  if val else None)
    floor                    = property( bidict({}),lambda val : int(val.replace('+',''))  if val else None)
    dollar_price             = property( bidict({}),lambda val : int(val.replace(',',''))  if val else None)
    dram_price               = property( bidict({}),lambda val : int(val.replace(',',''))  if val else None)
    ruble_price              = property( bidict({}),lambda val : int(val.replace(',',''))  if val else None)
    city                     = property( bidict({}),lambda val : val if val else None)   #'Yerevan': -25.0, 'Ереван'
    street                   = property( bidict({}),lambda val : val if val else None)   #'Улица Гюлбенкяна'
    number_of_guests         = property( bidict({}),lambda val : int(val[0])  if val else None)
    land_area                = property( bidict({}),lambda val : int(val.split('_')[0].replace(',',''))  if val else None)
    room_area                = property( bidict({}),lambda val : int(val.split('_')[0])  if val else None)
    userid                   = property( bidict({}),lambda val : int(val)  if val else None)
    posted_date              = property( bidict({}),lambda val : val if val else None)
    update_date              = property( bidict({}),lambda val : val if val else None)
    closed_item              = property( bidict({'active':0, 'closed':1}))
    monthly_or_daily         = property( bidict({'monthly':1, 'daily':2}))

    @staticmethod
    def get(key, value) -> int:
        return getattr(HouseProperties, key, HouseProperties.default).get(value)
    
    @staticmethod
    def inverseGet(value, key):
        return getattr(HouseProperties, key, HouseProperties.default).inverse(value)
    
    @staticmethod
    def getColumnNames():
        columns = []
        for name, obj in HouseProperties.__dict__.items():
            if type(obj) is property:
                if name != 'default':
                    columns.append(name)
        return columns
