import sqlite3

connection = sqlite3.connect('database.db')
test_connection = sqlite3.connect('test.db')

with open('schema.sql') as f:
    schema = f.read()
    connection.executescript(schema)
    test_connection.executescript(schema)

connection.commit()
test_connection.commit()

connection.close()
test_connection.close()