import os
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Create a database connection to the SQLite database.

    `SQLite tutorial for creating a database.
    <https://www.sqlitetutorial.net/sqlite-python/creating-database/>`_

    :param db_file: (str) path to database file
    :return: Connection object or None
    """

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        raise e

def create_table(conn, create_table_sql):
    """Create a table from using SQL string.

    `SQLite tutorial for creating a table.
    <https://www.sqlitetutorial.net/sqlite-python/create-tables/>`_

    :param conn: Connection object
    :param create_table_sql: (str) a CREATE TABLE statement
    """

    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)

        cur.execute("SELECT name FROM sqlite_temp_master WHERE type='table';")
        return 0

    except Error as e:
        raise e


def insert_row(conn, table_name, key_value_pairs):
    """Insert a row into a specified table.

    `Based on the SQLite tutorial for table insertions.
    <https://www.sqlitetutorial.net/sqlite-python/insert/>`_

    :param conn: Connection object
    :param table_name: (str) name of table for row insertion
    :param key_value_pairs: (dict) dictionary of key value pairs
    :return: (int) row_id
    """

    keys = sorted(key_value_pairs.keys())
    values = tuple([key_value_pairs[key] for key in keys])
    sql = '''INSERT INTO {0}({1}) VALUES({2})'''.format(
        table_name, ','.join(keys), ','.join('?' for _ in keys))

    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid


def select_rows(conn, table_name, key_search_value_list):
    """Query table using specific keys, values, and search types.

    `Based on the SQLite tutorial for record selection.
    <https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/>`_

    :param conn:  Connection object
    :param table_name: (str) name of table to be queried
    :param key_search_value_list: list of tuples [(column_name, search_type, value)],
                                  Valid search_types: '<', '<=', '=', '>=', '>', '!='
    :return: list of result tuples
    """

    cur = conn.cursor()

    search_criteria_str = ''
    search_criteria_values = []

    for key, search_type, value in key_search_value_list:
        search_criteria_str += '{0} {1} ? AND '.format(key, search_type)
        search_criteria_values.append(value)

    # drop the last AND
    search_criteria_str = search_criteria_str[:-5]

    sql = "SELECT * FROM {0} WHERE {1}".format(table_name, search_criteria_str)

    cur.execute(sql, search_criteria_values)

    rows = cur.fetchall()

    return rows


def update_row(conn, table_name, row_id, key_value_pairs):
    """Update value in a specified table based on table id.

    `Based on the SQLite tutorial for record update.
    <https://www.sqlitetutorial.net/sqlite-python/update/>`_

    :param conn: Connection object
    :param table_name: (str) name of table needing update
    :return: (int) row id
    """

    keys = sorted(key_value_pairs.keys())
    set_str = ' = ? , '.join(keys) + ' = ?'
    values = tuple([key_value_pairs[key] for key in keys] + [row_id])

    sql = '''UPDATE {0} SET {1} WHERE id = ?'''.format(table_name, set_str)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()


def delete_rows(conn, table_name, key_search_value_list):
    """Delete from table using specific keys, values, and search types.

    :param conn: Connection object
    :param table_name: (str) name of table requiring row deletion
    :param key_search_value_list: list of tuples, [(column_name, search_type, value)],
                                  Valid search_types: '<', '<=', '=', '>=', '>', '!='
    :return: list of result tuples
    """

    cur = conn.cursor()

    initial_row_count = cur.execute("SELECT COUNT (*) FROM {0}".format(table_name)).fetchone()[0]

    search_criteria_str = ''
    search_criteria_values = []

    for key, search_type, value in key_search_value_list:
        search_criteria_str += '{0} {1} ? AND '.format(key, search_type)
        search_criteria_values.append(value)

    # drop the last AND
    search_criteria_str = search_criteria_str[:-5]

    sql = "DELETE FROM {0} WHERE {1}".format(table_name, search_criteria_str)

    cur.execute(sql, search_criteria_values)
    conn.commit()

    final_row_count = cur.execute("SELECT COUNT (*) FROM {0}".format(table_name)).fetchone()[0]

    return initial_row_count - final_row_count


def delete_table(conn, table_name):
    """Delete table from database.

    :param conn: Connection Object
    :param table_name: (str) name of table to be deleted
    """

    try:
        cur = conn.cursor()
        cur.execute('DROP TABLE {0}'.format(table_name))
        return 0
    except Error as e:
        raise e


def delete_database(database_name):
    """Delete database by deleting the file.

    :param database_name: (str) name of database to be deleted
    """

    # close existing connections to the database
    conn = create_connection(database_name)
    conn.close()

    if os.path.isfile(database_name):
        try:
            os.remove(database_name)
        except Error as e:
            raise e
