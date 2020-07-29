import sqlite3
import re

from mileage import Mileage


SOURCE_DB = 'db/obiekt_kolejowy.tdb2'
#SOURCE_DB = 'db/test_db.db'
TABLE = 'przebiegi'
RE = r"^[a-zA-Z0-9_]+$"


class QueryError(Exception):
    pass

class Query():

    #def __init__(self, database: str, table: str):
    def __init__(self):
        self.database = SOURCE_DB
        table = TABLE
        self.c = sqlite3.connect(self.database)
        self.table = table

    def validate_parameter(self, parameter: str):
        ''' Sqlite3 uses its own parameters to make a query,
            but it does not allow to parameterize table argument.'''
        if re.match(RE, parameter) is None:
            raise QueryError("Query parameter contain not allowed characters. "\
                "Allowed characters are: A-Z, a-z, 0-9, _")

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table_name: str):
        self.validate_parameter(table_name)
        self._table = table_name

    def get_tables_names(self):
        query = f"SELECT name FROM sqlite_master "\
            f"WHERE type = 'table'"
        return self.c.execute(query).fetchall()

    def get_column_names(self):
        query = f"PRAGMA table_info({self.table});"
        return self.c.execute(query).fetchall()

    def get_all_mileage(self):
        query = f"SELECT * FROM {self.table};"
        return self.c.execute(query).fetchall()

    def get_end_semaphore_list(self, start_semaphore: str):
        self.validate_parameter(start_semaphore)
        query = f"SELECT id,semafor_koncowy FROM {self.table} "\
            f"WHERE semafor_poczatkowy = '{start_semaphore}'"
        return self.c.execute(query).fetchall()

    def find_mileage(self, mileage_id=None, start=None, end=None):
        too_many_arguments_error_msg = "Only one argument should be set."
        missing_argument_error_msg = "One of the argumens have to be set."

        if mileage_id:
            if start is not None or end is not None:
                raise QueryError(too_many_arguments_error_msg)
            parameter = 'id'
            value = mileage_id
        elif start:
            if end is not None:
                raise QueryError(too_many_arguments_error_msg)
            parameter = 'semafor_poczatkowy'
            value = start
        elif end:
            parameter = 'semafor_koncowy'
            value = end
        else:
            raise QueryError(missing_argument_error_msg)

        query = f"SELECT * FROM {self.table} " \
            f"WHERE {parameter} = '{value}';"
        return self.c.execute(query).fetchall()
