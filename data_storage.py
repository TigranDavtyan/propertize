import ast
import datetime
import shutil
import sqlite3 as lite
import gspread

nullable_columns = ['location','construction_type','new_construction','elevator','balcony','furniture','renovation','children_are_welcome','pets_allowed','utility_payments','prepayment','type','condition','garage','exterior_finish','location_from_the_street','entrance','lease_type','minimum_rental_period','interior_finishing','mortgage_is_possible','handover_date','floor_area','floors_in_the_building','number_of_bathrooms','number_of_rooms','ceiling_height','floor','city','street','number_of_guests','land_area','room_area','userid','monthly_or_daily']

def fillNone(item):
    for nc in nullable_columns:
        if nc not in item.keys():
            item[nc] = None
    return item

class DataDatabase:
    def __init__(self, path):
        self.conn = lite.connect(path)
        self.cur = self.conn.cursor()

        self.createTables()

        self.gc = gspread.service_account('C:/Users/Admin/Downloads/propertize-393618-2163bcf5743d.json')
        self.sheet = self.gc.open("propertize").sheet1


    def createTables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS listings (itemid INTEGER PRIMARY KEY, categoryid INTEGER, website TEXT,
                            location TEXT,
                            construction_type TEXT,
                            new_construction TEXT,
                            elevator TEXT,
                            balcony TEXT,
                            furniture TEXT,
                            renovation TEXT,
                            children_are_welcome TEXT,
                            pets_allowed TEXT,
                            utility_payments TEXT,
                            prepayment TEXT,
                            type TEXT,
                            condition TEXT,
                            garage TEXT,
                            exterior_finish TEXT,
                            location_from_the_street TEXT,
                            entrance TEXT,
                            lease_type TEXT,
                            minimum_rental_period TEXT,
                            interior_finishing TEXT,
                            mortgage_is_possible TEXT,
                            handover_date TEXT,
                            floor_area REAL,
                            floors_in_the_building INTEGER,
                            number_of_bathrooms INTEGER,
                            number_of_rooms INTEGER,
                            ceiling_height REAL,
                            floor INTEGER,
                            city TEXT,
                            street TEXT,
                            number_of_guests INTEGER,
                            land_area REAL,
                            room_area REAL,
                            userid INTEGER,
                            monthly_or_daily TEXT,
                dollar_price REAL, original_price REAL,posted_date DATETIME, update_date DATETIME, closed_item INTEGER, updates TEXT DEFAULT '{}')''')
        
    def query(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()
    def fetchone(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()
    def fetchall(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def createBackup(self):
        shutil.copy2('./data.db','./data.db.backup')
    def restoreBackup(self):
        shutil.copy2('./data.db.backup','./data.db')
        
    def insertOrUpdateListing(self, item):
        '''same - 0  |  updated - 1'''
        item = fillNone(item)
        item_db = self.fetchone('SELECT itemid, original_price, updates FROM listings WHERE itemid = ?;', (item['itemid'],))
        if item_db:
            if item_db[1] != item['original_price']:

                updates = ast.literal_eval(item_db[2])
                updates[str(item['update_date'])] = item['original_price']
                self.query("""UPDATE listings SET original_price = ?, dollar_price = ?, update_date = DATETIME('now'), updates = ?
                  WHERE itemid = ?""", (item['original_price'], item['dollar_price'], str(updates), item['itemid']))
                return 1
            else:
                db.query('UPDATE listings SET closed_item = 0 WHERE itemid = ?;',(item['itemid'],))
                return 0
        else:
            updates = {str(item['update_date']):item['original_price']}
            self.query("INSERT INTO listings VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (item['itemid'], 
                        item['categoryid'],
                        item['website'],
                        item['location'],
                        item['construction_type'],
                        item['new_construction'],
                        item['elevator'],
                        item['balcony'],
                        item['furniture'],
                        item['renovation'],
                        item['children_are_welcome'],
                        item['pets_allowed'],
                        item['utility_payments'],
                        item['prepayment'],
                        item['type'],
                        item['condition'],
                        item['garage'],
                        item['exterior_finish'],
                        item['location_from_the_street'],
                        item['entrance'],
                        item['lease_type'],
                        item['minimum_rental_period'],
                        item['interior_finishing'],
                        item['mortgage_is_possible'],
                        item['handover_date'],
                        item['floor_area'],
                        item['floors_in_the_building'],
                        item['number_of_bathrooms'],
                        item['number_of_rooms'],
                        item['ceiling_height'],
                        item['floor'],
                        item['city'],
                        item['street'],
                        item['number_of_guests'],
                        item['land_area'],
                        item['room_area'],
                        item['userid'],
                        item['monthly_or_daily'],
                        item['dollar_price'],item['original_price'],item['posted_date'],item['update_date'],item['closed_item'], str(updates)))
            return 1
        
    def closeItem(self, itemid):
        updates = ast.literal_eval(self.fetchone('SELECT updates FROM listings WHERE itemid = ?;', (itemid,))[0])

        updates[str(datetime.datetime.now().date())] = -1

        self.query("UPDATE listings SET closed_item = 1, update_date = DATETIME('now'), updates = ? WHERE itemid = ?", (str(updates), itemid))

    def updateSheet(self):
        data = db.fetchall('SELECT * FROM listings;')
        self.sheet.clear()

        self.sheet.insert_row([info[1] for info in db.fetchall("PRAGMA table_info(listings)")])
        return self.sheet.insert_rows(data, row=2)
        

db = DataDatabase('data.db')