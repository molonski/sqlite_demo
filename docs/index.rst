.. SQLite_Demo documentation master file, created by
   sphinx-quickstart on Thu Sep  3 15:40:26 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SQLite_Demo's documentation!
=======================================

**SQLite_Demo** is a simple python package that interacts with SQLite Databases. It was created by
Chris Moloney to serve as demonstration of code, documentation, and unit testing.


Database Interaction Methods:
-----------------------------
The following CRUD Database Methods are available in the :mod:`sqlite_demo.db_interactions` module.


- :meth:`db_interactions.create_connection()<sqlite_demo.db_interactions.create_connection>` - Create a database and open a connection.
- :meth:`db_interactions.create_table()<sqlite_demo.db_interactions.create_table>` - Create a database table.
- :meth:`db_interactions.insert_row<sqlite_demo.db_interactions.insert_row>` - Insert a record in the database table.
- :meth:`db_interactions.update_row<sqlite_demo.db_interactions.update_row>` - Update a record in the database table.
- :meth:`db_interactions.select_rows<sqlite_demo.db_interactions.select_rows>` - Select records from a database table.
- :meth:`db_interactions.delete_rows<sqlite_demo.db_interactions.delete_rows>` - Delete records from a database table.
- :meth:`db_interactions.delete_table<sqlite_demo.db_interactions.delete_table>` - Delete a database table.
- :meth:`db_interactions.delete_database<sqlite_demo.db_interactions.delete_database>` - Delete a database.


.. toctree::
   :maxdepth: 2
   :caption:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
