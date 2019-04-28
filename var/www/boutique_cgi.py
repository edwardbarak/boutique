#!/usr/bin/python3

import cgi
import cgitb; cgitb.enable()

print('Content-type:text/html')
print()

import peewee as pw
from datetime import datetime
from main import rooms, customers, events

# TODO: Create function that gives the snackbar notification
def snackbar(tableSelect):
    # 'Created entry new entry in {}'.format(tableSelect)
    pass

with open('boutique_cgi.html', 'r') as f:
    print(f.read())
    f.close()

form = cgi.FieldStorage()
tableSelect = form.getvalue('table')

db = pw.MySQLDatabase(host='localhost', user='null', database='boutique')
cursor = db.cursor()

if tableSelect == 'rooms':
    rooms.create(
        roomType=form.getvalue('roomType'),
        price=form.getvalue('price'),
        discount=form.getvalue('discount'),
        roomPhoto=form.getvalue('roomPhoto'),
    )
    
    # Notify that entry has been created
    snackbar(tableSelect)

elif tableSelect == 'customers':
    checkIn = datetime(
        form.getvalue('checkInYear'),
        form.getvalue('checkInMonth'),
        form.getvalue('checkInDay'),
        form.getvalue('checkInHour'),
    )
    checkOut = datetime(
        form.getvalue('checkOutYear'),
        form.getvalue('checkOutMonth'),
        form.getvalue('checkOutDay'),
        form.getvalue('checkOutHour'),
    )

    customers.create(
        firstName=form.getvalue('firstName'),
        lastName=form.getvalue('lastName'),
        customerType=form.getvalue('customerType'),
        roomType=form.getvalue('roomType'),
        roomNum=form.getvalue('roomNum'),
        checkIn=checkIn,
        checkOut=checkOut,
        paymentMethod=form.getvalue('paymentMethod'),
    )

    # Notify that entry has been created
    snackbar(tableSelect)

elif tableSelect == 'events':
    eventStart = datetime(
        form.getvalue('eventStartYear'),
        form.getvalue('eventStartMonth'),
        form.getvalue('eventStartDay'),
        form.getvalue('eventStartHour'),
    )
    eventEnd = datetime(
        form.getvalue('eventEndYear'),
        form.getvalue('eventEndMonth'),
        form.getvalue('eventEndDay'),
        form.getvalue('eventEndHour'),
    )

    events.create(
        primaryCustomer=form.getvalue(''),
        eventName=form.getvalue('eventName'),
        eventStart=eventStart,
        eventEnd=eventEnd,
        participantCount=form.getvalue('participantCount'),
        specialRoomReqs=form.getvalue('specialRoomReqs'),
        paymentMethod=form.getvalue('paymentMethod'),
        notes=form.getvalue('notes'),
    )

    # Notify that entry has been created
    snackbar(tableSelect)

# TODO: Write output to new window
elif tableSelect == 'search':
    sql = 'SELECT * FROM customers WHERE lastName = {}'.format(form.getvalue('lastName'))
    cursor.execute(sql)

    # Fetch all the rows using fetchall() method.
    _data = cursor.fetchall()

    # Get column headers of query
    _cols = '\n'.join(['<th>{}</th>'.format(col[0]) for col in cursor.description])

    # Sort data into a table
    _tabledData = [ ['<th>{}</th>'.format(el) for el in row] for row in _data]
    _tabledData = ['<tr>{}</tr>'.format('\n'.join(row)) for row in _tabledData]
    _data = '\n'.join(_tabledData)

    table = """
    <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp">
        <thead>
            <tr>
                {cols}
            </tr>
        </thead>
        <tbody>
            {data}
        </tbody>
    </table>
    """.format(cols=_cols, data=_data)

    print(table)
else:
    print('<h1>tableSelect ERROR</h1>')

# disconnect from server
db.close()