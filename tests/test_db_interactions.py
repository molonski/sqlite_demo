import unittest
import os
import sys
import sqlite3

sys.path.append(os.path.abspath('..'))
print(os.path.abspath('..'))

import sqlite_demo.db_interactions as dbi


DB_NAME = 'unittest_database'
TABLE_NAME = 'test_table'
TEST_TABLE_SQL = """CREATE TABLE IF NOT EXISTS {0} (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        start_date text
                    ); """.format(TABLE_NAME)
ROW_DATA = {'name': 'Bob', 'start_date': '2021-01-01'}
SELECT_DATA = [('name', '=', 'Bob')]
CHANGE_DATA = {'start_date': '2021-02-01'}


class TestSQLiteFunctions(unittest.TestCase):

    @staticmethod
    def _query_tables():
        """query table names using SQL equivalent to the sqlite3 .tables command"""

        conn = dbi.create_connection(DB_NAME)
        cur = conn.cursor()
        cur.execute("""SELECT name FROM sqlite_master
                               WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'
                               UNION ALL
                               SELECT name FROM sqlite_temp_master
                               WHERE type IN ('table','view')
                               ORDER BY 1""")
        return cur.fetchall()

    @staticmethod
    def _set_up_test_database(table_sql=None, add_row=None):
        """Utility function to set up a test database for each unit test."""

        conn = dbi.create_connection(DB_NAME)
        if table_sql:
            dbi.create_table(conn, table_sql)
        if add_row:
            dbi.insert_row(conn, TABLE_NAME, add_row)
        return conn

    @staticmethod
    def _delete_test_database():
        """Remove the test database at the end of each test."""
        dbi.delete_database(DB_NAME)

    def test_create_connection(self):
        conn = self._set_up_test_database()

        self.assertTrue(os.path.isfile(DB_NAME))
        self.assertTrue(isinstance(conn, sqlite3.Connection))

        self._delete_test_database()

    def test_create_table(self):
        conn = self._set_up_test_database()

        bad_sql = """CREATE TABLE IF NOT EXISTS fail_table (
                        id integer PRIMARY KEY,
                        this will throw an error, oh no!!!!!
                    ); """

        with self.assertRaises(sqlite3.OperationalError):
            dbi.create_table(conn, bad_sql)

        self.assertEqual(dbi.create_table(conn, TEST_TABLE_SQL), 0)

        result = self._query_tables()
        self.assertTrue(TABLE_NAME in str(result))

        self._delete_test_database()

    def test_insert_row(self):
        conn = self._set_up_test_database(table_sql=TEST_TABLE_SQL)

        row_ind = dbi.insert_row(conn, TABLE_NAME, ROW_DATA)
        self.assertEqual(row_ind, 1)

        self._delete_test_database()

    def test_select_rows(self):
        conn = self._set_up_test_database(table_sql=TEST_TABLE_SQL, add_row=ROW_DATA)

        rows = dbi.select_rows(conn, TABLE_NAME, SELECT_DATA)
        self.assertEqual(len(rows), 1)
        self.assertTrue(isinstance(rows[0], tuple))
        self.assertEqual(rows[0][0], 1)
        self.assertEqual(rows[0][1], 'Bob')

        self._delete_test_database()

    def test_update_row(self):
        conn = self._set_up_test_database(table_sql=TEST_TABLE_SQL, add_row=ROW_DATA)

        dbi.update_row(conn, TABLE_NAME, 1, CHANGE_DATA)
        rows = dbi.select_rows(conn, TABLE_NAME, SELECT_DATA)
        self.assertEqual(rows[0][2], CHANGE_DATA['start_date'])

        self._delete_test_database()

    def test_delete_table(self):
        conn = self._set_up_test_database(table_sql=TEST_TABLE_SQL)

        dbi.delete_table(conn, TABLE_NAME)
        result = self._query_tables()

        self.assertTrue(TABLE_NAME not in str(result))

        self._delete_test_database()

    def test_delete_database(self):

        _ = self._set_up_test_database()

        self.assertTrue(os.path.isfile(DB_NAME))

        self._delete_test_database()

        self.assertFalse(os.path.isfile(DB_NAME))


if __name__ == '__main__':
    unittest.main()
