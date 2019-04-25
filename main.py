#!/usr/bin/env python3

import peewee as pw
from playhouse.dataset import DataSet
from playhouse.db_url import connect

# Variables
database='boutique'
host='localhost'
user='null'

dbURL = 'mysql://{user}@{host}/{database}'.format(database=database, host=host, user=user)
db = connect(dbURL)
dbDataset = DataSet(dbURL)

# Models (Table Schema)
class BaseModel(pw.Model):
    class Meta:
        database = db

class rooms(pw.Model):
    roomType = pw.TextField()
    price = pw.FloatField()
    roomNum = pw.IntegerField()
    discount = pw.TextField()
    roomPhoto = pw.TextField()
    
    class Meta:
        database = db

class customers(pw.Model):
    firstName = pw.TextField()
    lastName = pw.TextField()
    customerType = pw.TextField()   # primary or dependent
    roomNum = pw.IntegerField()
    checkIn = pw.DateTimeField()
    checkOut = pw.DateTimeField()
    paymentMethod = pw.TextField()
    eventID = pw.IntegerField()

    class Meta:
        database = db

class events(pw.Model):
    primaryCustomer = pw.IntegerField()
    eventName = pw.TextField()
    eventType = pw.TextField()
    eventStart = pw.DateTimeField()
    eventEnd = pw.DateTimeField()
    participantCount = pw.IntegerField()
    specialRoomReqs = pw.TextField()
    paymentMethod = pw.TextField()
    notes = pw.TextField()

    class Meta:
        database = db

# Functions

def create_tables(db, tables):
    db.create_tables(tables)
    print('Created tables {}').format(tables)

# Main
if __name__ == "__main__":
    notice = """'Current default settings:
    Database: {database}
    Host: {host}
    User:{user}
    
    NOTE: If you want to change these defaults you can do so on lines 7 - 9 of this file (db_funcs.py)
    """.format(database=database, host=host, user=user)
    print(notice)
    
    if input('Create table schemas? (y/n)').lower() == 'y':
        # Create table schemas
        create_tables(db, [rooms, customers, events])
        
    if input('Load data into tables? (y/n)').lower() == 'y':
        # Load data into tables
            
    db.close()