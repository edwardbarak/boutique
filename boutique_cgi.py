#!/usr/bin/python3

import cgi
import cgitb; cgitb.enable()

print('Content-type:text/html')
print()

import peewee as pw

with open('boutique_cgi.html', 'r') as f:
    print(f.read())
    f.close()

form = cgi.FieldStorage()
sql = form.getvalue('fname')

db = pw.MySQLDatabase(host='localhost', user='null', database='boutique')
cursor = db.cursor()
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

# disconnect from server
db.close()