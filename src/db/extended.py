from __future__ import annotations

import sqlite3
from typing import Sequence


class Database:
    @staticmethod
    def connect(name: str) -> sqlite3.Connection:
        """Returns a connection to a database.

        If the database does not exist it will create one before
        returning a connection.

        Args:
            name (str): name of the database.
        Returns:
            sqlite3.Connection: connection to database.
        """

        return sqlite3.connect(database=name)

    @staticmethod
    def execute_and_confirm(connection: sqlite3.Connection,
                            query: str,
                            data: Sequence = None,
                            many: bool = False) -> bool:
        """Executes a query and returns whether it was successful.

        Args:
            connection (sqlite3.Connection): object connected to database.
            query (str): the query to execute.
            data (Sequence): a sequence of values.
            many (bool): set to True if passing in many rows to insert.
        Returns:
            bool: True if query executed successfully otherwise False.
        """

        return True if Database.execute_and_retrieve(connection, query, data, many) else False

    @staticmethod
    def execute_and_retrieve(connection: sqlite3.Connection,
                             query: str,
                             data: Sequence = None,
                             many: bool = False) -> sqlite3.Cursor:
        """Executes a query and returns the result.

        Args:
            connection (sqlite3.Connection): object connected to database.
            query (str): the query to execute.
            data (Sequence): a sequence of values.
            many (bool): set to True if passing in many rows to insert.
        Returns:
            sqlite3.Cursor: the Cursor object.
        """

        with connection:
            result = None

            try:
                cursor = connection.cursor()

                if not data:
                    result = cursor.execute(query)
                else:
                    if many:
                        values = [(value,) for value in data]
                        result = cursor.executemany(query, values)
                    else:
                        if len(data) > 1:
                            result = cursor.execute(query, data)
                        else:
                            result = cursor.execute(query, (data[0],))
                connection.commit()
            except sqlite3.Error as error:
                print(f"Error: {Database.execute_and_retrieve.__name__} {error}")
            except IndexError as error:
                print(f"Error: {error}")
            return result

    @staticmethod
    def create_table(connection: sqlite3.Connection, data: dict) -> bool:
        """Creates a table with the structure specified by the dict.

        The dict needs to have a particular structure for this to work:
        {
            "name": <table_name>,
            "columns": {
                "name": "<data_type> <constraints>"
                ...
            }
        }

        Args:
            connection (sqlite3.Connection): object connected to database.
            data (dict): table specifications.
        Returns:
            bool: True if operation was successful otherwise False.
        """

        columns = [f"{col_name} {col_type}" for col_name, col_type in data["columns"].items()]
        query = f"CREATE TABLE IF NOT EXISTS {data['name']} ({', '.join(columns)});"
        return Database.execute_and_confirm(connection, query)

    @staticmethod
    def create_table_from_file(connection: sqlite3.Connection, path: str) -> bool:
        """Creates a table from a sql file by the path provided.

        Args:
            connection (sqlite3.Connection): object connected to database.
            path (str): path to file.
        Returns:
            bool: True if operation was successful otherwise False.
        """

        with open(path, "r", encoding="utf-8") as file_in:
            try:
                connection.executescript(file_in.read())
                connection.commit()
            except sqlite3.Error as error:
                print(f"Error: {error}")
                return False
            else:
                return True

    @staticmethod
    def insert_single_col_into_table(connection: sqlite3.Connection,
                                     table: str,
                                     col: str,
                                     data: Sequence,
                                     many: bool = False) -> sqlite3.Cursor:
        """Insert a row of a single column into a table.

        Args:
            connection (sqlite3.Connection): object connected to database.
            table (str): name of the table to insert data into.
            col (str): name of the column.
            data (Sequence): a sequence of values.
            many (bool): set to True if passing in many rows to insert.
        Returns:
            bool: True if operation was successful otherwise False.
        """

        query = f"INSERT INTO {table} ({col}) VALUES (?);"
        return Database.execute_and_retrieve(connection, query, data, many=many)

    @staticmethod
    def insert_multiple_col_into_table(connection: sqlite3.Connection,
                                       table: str,
                                       cols: Sequence[str],
                                       data: Sequence,
                                       many: bool = False) -> sqlite3.Cursor:
        """Insert a row of multiple columns into a table.

        Args:
            connection (sqlite3.Connection): object connected to database.
            table (str): name of the table to insert data into.
            cols (str): name of the column.
            data (Sequence[str]): a sequence of column names.
            many (bool): set to True if passing in many rows to insert.
        Returns:
            bool: True if operation was successful otherwise False.
        """

        columns = ", ".join(cols)
        values = ", ".join(["?" for _ in cols])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"
        return Database.execute_and_retrieve(connection, query, data, many)

    @staticmethod
    def find_by_pk(connection: sqlite3.Connection,
                   table: str,
                   pk_col: str,
                   pk: int) -> tuple:
        """Searches a table by the name of the column for a row where id matches pk.

        Args:
            connection (sqlite3.Connection): object connected to database.
            table (str): name of the table to search from.
            pk_col (str): the name of the primary key column.
            pk (int): the primary key or id to search for.
        Returns:
            tuple: a row in the searched table if found or None if not found.
        """

        query = f"SELECT * FROM {table} WHERE {pk_col} = {pk};"
        return connection.cursor().execute(query).fetchone()

    @staticmethod
    def find_one_in_col_by_this(connection: sqlite3.Connection,
                                table: str,
                                col: str,
                                this: object) -> tuple:
        """Searches a table for one row that matches the search parameter.

        Searches a table where the specified value (this) matches
        the value of a column (col) in a row.

        Args:
            connection (sqlite3.Connection): object connected to database.
            table (str): name of the table to search from.
            col (str): the name of the column to compare to.
            this (object): the value to match by.
        Returns:
            tuple: a row in the searched table if found or None if not found.
        """

        query = f"SELECT * FROM {table} WHERE {col} = {this};"
        return connection.cursor().execute(query).fetchone()

    @staticmethod
    def find_all_in_col_by_this(connection: sqlite3.Connection,
                                table: str,
                                col: str,
                                this: object) -> list[tuple]:
        """Searches a table for many rows that matches the search parameter.

        Searches a table for rows where the specified value (this) matches
        the value of a column (col).

        Args:
            connection (sqlite3.Connection): object connected to database.
            table (str): name of the table to search from.
            col (str): the name of the column to compare to.
            this (object): the value to match by.
        Returns:
            list[tuple]: a list of rows in the searched table if found otherwise empty List.
        """

        query = f"SELECT * FROM {table} WHERE {col} = {this};"
        return connection.cursor().execute(query).fetchall()
