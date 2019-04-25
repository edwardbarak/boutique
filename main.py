#!/usr/bin/env python3

import peewee as pw
from playhouse.dataset import DataSet
from playhouse.db_url import connect
from random import randint

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
    discount = pw.FloatField()
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

def generate_data(n=10):
    # rooms
    roomTypes = ['single', 'double', 'queen', 'king']
    rooms.create(type='single', 
        price=200, 
        discount=1,
        roomPhoto='./images/single.jpg'
        )
    rooms.create(type='double', 
        price=300, 
        discount=.95,
        roomPhoto='./images/double.jpg'
        )
    rooms.create(type='queen', 
        price=400, 
        discount=.9,
        roomPhoto='./images/queen.jpg'
        )
    rooms.create(type='king', 
        price=500, 
        discount=.85,
        roomPhoto='./images/king.jpg'
        )

    # customers
    firstNames = ['John', 'Jane', 'Jim', 'Kelly']
    lastNames = ['Doe', 'Brown', 'White', 'Black']
    roomNums = list(range(100, 100+n))
    for i in range(n):
        newCustomer = {
            'firstName': firstNames[randint(0,len(firstNames))],
            'lastName': lastNames[randint(0,len(firstNames))],
            'customerType': 'primary',
            'roomType': roomTypes[randint(0,len(roomTypes))],
            'roomNum': roomNums.pop(randint(0,len(roomNums)))
        }
        

    """
    STOCK.create(ticker='DWDP', exchange='NYSE')

    customers.firstName = pw.TextField()
    customers.lastName = pw.TextField()
    customers.customerType = pw.TextField()
    customers.roomNum = pw.IntegerField()
    customers.checkIn = pw.DateTimeField()
    customers.checkOut = pw.DateTimeField()
    customers.paymentMethod = pw.TextField()
    customers.eventID = pw.IntegerField()

    events.primaryCustomer = pw.IntegerField()
    events.eventName = pw.TextField()
    events.eventType = pw.TextField()
    events.eventStart = pw.DateTimeField()
    events.eventEnd = pw.DateTimeField()
    events.participantCount = pw.IntegerField()
    events.specialRoomReqs = pw.TextField()
    events.paymentMethod = pw.TextField()
    events.notes = pw.TextField()
    """

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
        # generate data
        
        # load data into tables
        pass
            
    db.close()