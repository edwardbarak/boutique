#!/usr/bin/env python3

import peewee as pw
from playhouse.dataset import DataSet
from playhouse.db_url import connect
from random import randint, choice

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

def generate_data(n=10):
    # rooms
    roomTypes = ['single', 'double', 'queen', 'king', 'event']
    p = 200 # initial price
    d = 1.0 # percentage of list price discout will reduce to

    for room in roomTypes:
        rooms.create(type=room,
            price=p,
            discount=d,
            roomPhoto='./images/{}.jpg'.format(room)
        )
        p += 100
        d -= 0.05

    # customers
    import datetime

    firstNames = ['John', 'Jane', 'Jim', 'Kelly', 'Megan', 'Chris']
    lastNames = ['Doe', 'Brown', 'White', 'Black', 'Price', 'Baker']
    paymentTypes = ['Debit Card', 'Credit Card', 'Cash', 'Paypal']
    
    roomNums = list(range(100, 100+n))
    today = datetime.datetime.now()

    for i in range(n):
        newCustomer = {
            'firstName': choice(firstNames),
            'lastName': choice(lastNames),
            'customerType': 'primary',
            'roomType': choice(roomTypes),
            'roomNum': roomNums.pop(randint(0,len(roomNums))),
            'checkIn': datetime.datetime(today.year, today.month, today.day, 8) + datetime.timedelta(days=randint(0,7)),
            'paymentMethod': choice(paymentTypes),
            }
        # dependent variables
        newCustomer['checkOut'] = newCustomer['checkIn'] + datetime.timedelta(days=randint(0,4), hours=9)
        
        customers.create(
            firstName=newCustomer['firstName'],
            lastName=newCustomer['lastName'],
            customerType=newCustomer['customerType'],
            roomType=newCustomer['roomType'],
            roomNum=newCustomer['roomNum'],
            checkIn=newCustomer['checkIn'],
            checkOut=newCustomer['checkOut'],
            paymentMethod=newCustomer['paymentMethod'],
            )

    # events
    eventNames = [
        'Tinfoil Hat Convention', 
        'Dungeon and Dragons Competition',
        'Canadian Maple Syrup Consortium', 
        'Make America America Again!',
        ]
    specialRoomReqTypes = [
        'Quiet', 
        'Spacious', 
        None
        ]
    notes = [None, 'Customer is very particular.', 'Event could be loud.']

    customersTable = list(customers.select().dicts())
    
    for i in range(len(eventNames) - randint(1, len(eventNames) - 1)):
        selectedCustomer = customersTable.pop(randint(0,len(customersTable)))
        events.create(
            primaryCustomer = selectedCustomer['id'],
            eventName = eventNames.pop(randint(0,len(eventNames))),
            eventStart = selectedCustomer['checkIn'],
            eventEnd = selectedCustomer['checkOut'],
            participantCount = randint(3,100),
            specialRoomReqs = choice(specialRoomReqTypes),
            paymentMethod = choice(paymentTypes),
            notes = choice(notes),
        )

# Main
if __name__ == "__main__":
    notice = """'Current default settings:
    Database: {database}
    Host: {host}
    User:{user}
    """.format(database=database, host=host, user=user)
    
    print(notice)
    
    if input('Create table schemas? (y/n)').lower() == 'y':
        # Create table schemas
        tables = [rooms, customers, events]
        db.drop_tables(tables)
        print('Dropping table(s) if already in existence.')
        db.create_tables(tables)
        print('Created table(s).')
        
    if input('Create & load data into tables? (y/n)').lower() == 'y':
        # generate & load data
        generate_data()
            
    db.close()