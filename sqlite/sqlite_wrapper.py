import sqlite3
from flask import Flask, request
from sqlite3 import Error

app = Flask(__name__)

database = "addresses.db"
connection = None


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

    # Creates the table where non-leader nodes store the address of the next function
    create_addresses_table = ''' CREATE TABLE IF NOT EXISTS addresses(function TEXT, address TEXT); '''
    # Creates the table where non-leader nodes store the leader address of their group
    create_leader_table = ''' CREATE TABLE IF NOT EXISTS leaders(address TEXT) '''

    # Creates the table where leader nodes store information about nodes in their group
    create_grouping_info_table = ''' CREATE TABLE IF NOT EXISTS grouping(address TEXT, cpu TEXT, memory TEXT, functions TEXT, secret TEXT) '''

    try:
        c = conn.cursor()
        c.execute(create_addresses_table)
        c.execute(create_leader_table)
        c.execute(create_grouping_info_table)
    except Error as e:
        print(e)


@app.before_first_request
def before_first_request():
    global connection
    connection = create_connection(database)
    create_tables(connection)


# ----------- API endpoints (non-leaders) -----------------------


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


# ----------- API endpoints (leaders) -----------------------


@app.route('/add-node', methods=['POST'])
def add_node_endpoint():
    add_node(connection, (request.data.split(b',')))
    return 'New node added'


@app.route('/update-node', methods=['POST'])
def update_node_endpoint():
    update_node(connection, (request.data.split(b',')))
    return 'Node updated'


@app.route('/add-fn', methods=['POST'])
def add_fn_endpoint():
    add_fn(connection, (request.data.split(b',')))
    return 'Node updated'


@app.route('/get-alternatives', methods=['POST'])
def get_alternatives_endpoint():
    return get_alternatives(connection, request.data)


@app.route('/get-all-nodes', methods=['GET'])
def get_all_nodes_endpoint():
    return get_all_nodes(connection)


# ----------- SQLite operators (non-leaders) ----------------


def set_address(conn, data):
    """
    Delete old address (if exists) and set a new one for given function
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
    get_query = ''' SELECT address FROM addresses WHERE function=? '''
    cur = conn.cursor()
    cur.execute(get_query, (function_name,))
    res = cur.fetchall()
    if len(res) == 0:
        return ''
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

    get_query = ''' SELECT * FROM leaders '''
    cur = conn.cursor()
    cur.execute(get_query)
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


# ----------- SQLite operators (leaders) ----------------


def add_node(conn, node):
    """
    Add a node to the leader
    :param conn: sqlite connection
    :param node: node information
    """

    insert_query = ''' INSERT INTO grouping(address, cpu, memory, secret) VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(insert_query, node)
    conn.commit()


def update_node(conn, node_info):
    """
    Update a nodes information such as cpu and memory usage
    :param conn: sqlite connection
    :param node_info: new node information
    """

    update_query = ''' UPDATE grouping SET cpu=?, memory=? WHERE address=? '''
    cur = conn.cursor()
    cur.execute(update_query, (node_info[1], node_info[2], node_info[0]))
    conn.commit()


def add_fn(conn, fn_node_info):
    """
    Add a function to a node
    :param conn: sqlite connection
    :param fn_node_info: function name and node address
    """

    insert_query = ''' UPDATE grouping SET functions=IFNULL(functions, '') || ? || ',' WHERE address=? '''
    cur = conn.cursor()
    cur.execute(insert_query, fn_node_info)
    conn.commit()


def get_alternatives(conn, fn):
    """
    Find all nodes where the given function is deployed
    :param conn: sqlite connection
    :param fn: function name
    """

    get_query = ''' SELECT address FROM grouping WHERE INSTR(functions, ?) IS NOT 0 '''
    cur = conn.cursor()
    cur.execute(get_query, (fn,))
    fetched = cur.fetchall()
    res = ''
    for e in fetched:
        res += e[0].decode('utf-8') + ','
    return res[:-1]


def delete_node(conn, node):
    """
    TODO: Check if node is reachable. If not, delete it from database
    :param conn: sqlite connection
    :param node: inactive node
    """


def get_all_nodes(conn):
    """
    Retrieve all nodes inside the group
    :param conn: sqlite connection
    """

    get_query = ''' SELECT address, secret FROM grouping '''
    cur = conn.cursor()
    cur.execute(get_query)
    fetched = cur.fetchall()
    res = ''
    for e in fetched:
        res += e[0].decode('utf-8') + ' ' + e[1].decode('utf-8') + ','
    return res[:-1]


if __name__ == '__main__':
    app.run(host="0.0.0.0")
