import sqlite3
from flask import Flask, request
from sqlite3 import Error

app = Flask(__name__)

database = "addresses.db"
connection = None


# ------------- API endpoints -----------------


@app.before_first_request
def before_first_request():
    global connection
    connection = create_connection(database)
    create_tables(connection)


@app.route('/set-address', methods=['POST'])
def set_address_endpoint():
    set_address(connection, (request.data.split(b',')))
    return 'New address set'


@app.route('/get-address', methods=['POST'])
def get_address_endpoint():
    return get_address(connection, request.data)


@app.route('/set-leader-address', methods=['POST'])
def set_leader_address_endpoint():
    set_leader_address(connection, (request.data,))
    return 'New leader address set'


@app.route('/get-leader-address', methods=['GET'])
def get_leader_address_endpoint():
    return get_leader_address(connection)


# ----------- SQLite operators -------------------


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


def create_tables(conn):
    """ create needed tables if they do not exist
    :param conn: sqlite connection
    """
    create_addresses_table = ''' CREATE TABLE IF NOT EXISTS addresses(function TEXT, address TEXT); '''
    create_leader_table = ''' CREATE TABLE IF NOT EXISTS leaders(address TEXT) '''
    try:
        c = conn.cursor()
        c.execute(create_addresses_table)
        c.execute(create_leader_table)
    except Error as e:
        print(e)


def set_address(conn, data):
    """
    Delete old address (if exists) and set a new one
    :param conn: sqlite connection
    :param data: function name + the address where the function is deployed
    """
    delete_query = ''' DELETE FROM addresses WHERE function=? '''
    insert_query = ''' INSERT INTO addresses(function, address) VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(delete_query, (data[0],))
    cur.execute(insert_query, data)
    conn.commit()


def get_address(conn, function_name):
    """
    Retrieve address where the next function is deployed
    :param conn: sqlite connection
    :param function_name: function name to be queried
    """
    get_query = ''' SELECT address FROM addresses WHERE function=? LIMIT 1 '''
    cur = conn.cursor()
    cur.execute(get_query, (function_name,))
    res = cur.fetchall()
    return res[0][0]


def set_leader_address(conn, address):
    """
    Delete old leader address (if exists) and set a new one
    :param conn: sqlite connection
    :param address: leader address
    """
    delete_query = ''' DELETE FROM leaders '''
    insert_query = ''' INSERT INTO leaders(address) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(delete_query)
    cur.execute(insert_query, address)
    conn.commit()


def get_leader_address(conn):
    """
    Retrieve leader address (currently only one saved)
    :param conn: sqlite connection
    """
    get_query = ''' SELECT * FROM leaders LIMIT 1 '''
    cur = conn.cursor()
    cur.execute(get_query)
    res = cur.fetchall()
    return res[0][0]


if __name__ == '__main__':
    app.run(host="0.0.0.0")
