#!/usr/bin/python3

import cgi
import cgitb; cgitb.enable()

print('Content-type:text/html')
print()

import os
import peewee as pw
from datetime import datetime
from main import rooms, customers, events

def history(historyFilename, tableSelect):
    with open(historyFilename, 'w') as f:
        f.write(tableSelect)
        f.close()

historyFilename = './history.ini'
queryFilename = './query.csv'

with open('./boutique_cgi.html', 'r') as f:    
    html = f.read()

    if os.path.isfile(historyFilename):        
        with open(historyFilename) as hf:            
            confirmation = """
                <br>
                <p>    </p>
                <span class="mdl-chip mdl-chip--contact">
                    <span class="mdl-chip__contact mdl-color--teal mdl-color-text--white">!</span>
                    <span class="mdl-chip__text">Created new record in the {} table</span>
                </span>
            """.format(hf.read()[:-1])            
            print(html.replace('<!-- confirmation -->', confirmation))
            os.remove(historyFilename)

    elif os.path.isfile(queryFilename):
        # remove first tab as active tab
        html = html.replace('is-active', '')
        
        # make 4th tab the active tab
        html = html.replace('" id="fixed-tab-4">', ' is-active" id="fixed-tab-4">')
        
        # print query resuslts to 4th tab
        with open(queryFilename, 'r') as queryResults:
            html = html.replace('<!-- query resuslts -->', '<br>' + queryResults.read()) 
        os.remove(queryFilename)
        print(html)

    else:
        print(html)

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
    
    history(historyFilename, tableSelect)

elif tableSelect == 'customers':
    checkIn = datetime(
        int(form.getvalue('checkInYear')),
        int(form.getvalue('checkInMonth')),
        int(form.getvalue('checkInDay')),
        int(form.getvalue('checkInHour')),
        int(form.getvalue('checkInMinute')),
    )
    checkOut = datetime(
        int(form.getvalue('checkOutYear')),
        int(form.getvalue('checkOutMonth')),
        int(form.getvalue('checkOutDay')),
        int(form.getvalue('checkOutHour')),
        int(form.getvalue('checkOutMinute')),
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

    history(historyFilename, tableSelect)

elif tableSelect == 'events':
    eventStart = datetime(
        int(form.getvalue('eventStartYear')),
        int(form.getvalue('eventStartMonth')),
        int(form.getvalue('eventStartDay')),
        int(form.getvalue('eventStartHour')),
        int(form.getvalue('eventStartMinute')),
    )
    eventEnd = datetime(
        int(form.getvalue('eventEndYear')),
        int(form.getvalue('eventEndMonth')),
        int(form.getvalue('eventEndDay')),
        int(form.getvalue('eventEndHour')),
        int(form.getvalue('eventEndMinute')),
    )

    events.create(
        primaryCustomer=int(form.getvalue('primaryCustomer')),
        eventName=form.getvalue('eventName'),
        eventStart=eventStart,
        eventEnd=eventEnd,
        participantCount=int(form.getvalue('participantCount')),
        specialRoomReqs=form.getvalue('specialRoomReqs'),
        paymentMethod=form.getvalue('paymentMethod'),
        notes=form.getvalue('notes'),
    )

    history(historyFilename, tableSelect)

# TODO: Write output to new window
elif tableSelect == 'search':
    sql = 'SELECT * FROM customers WHERE lastName = "{}"'.format(form.getvalue('lastName'))
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

    with open(queryFilename, 'w') as f:
        f.write(table)
        f.close()
else:
    raise IOError('tableSelect ERROR')

# disconnect from server
db.close()