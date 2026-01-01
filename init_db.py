import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    schema = f.read()
    connection.executescript(schema)

connection.commit()

connection.close()