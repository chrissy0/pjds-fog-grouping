import sqlite3
from flask import Flask, request
from sqlite3 import Error

app = Flask(__name__)

database = "addresses.db"
connection = None


@app.before_first_request
def before_first_request():
    global connection
    connection = create_connection(database)
    create_table(connection)


@app.route('/set-address', methods=['POST'])
def set_address():
    print(request.data)
    set_address(connection, (request.data, ))
    return 'New address set'


@app.route('/get-address', methods=['GET'])
def get_address():
    return get_address(connection)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn):
    create_addresses_table = """ CREATE TABLE IF NOT EXISTS addresses(address TEXT); """
    try:
        c = conn.cursor()
        c.execute(create_addresses_table)
    except Error as e:
        print(e)


def set_address(conn, address):
    """
    Delete old address (if exists) and set a new one
    :param connection:
    :param address:
    :return:
    """
    delete_query = ''' DELETE FROM addresses '''
    insert_query = ''' INSERT INTO addresses(address) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(delete_query)
    cur.execute(insert_query, address)
    conn.commit()


def get_address(conn):
    get_query = ''' SELECT * FROM addresses LIMIT 1 '''
    cur = conn.cursor()
    cur.execute(get_query)
    res = cur.fetchall()
    return res[0][0]


if __name__ == '__main__':
    app.run()
