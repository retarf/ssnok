import sqlite3
import re


SOURCE_DB = 'db/obiekt_kolejowy.tdb2'
TABLE = 'przebiegi'
RE = r"^[a-zA-Z0-9_]+$"


class QueryError(Exception):
    pass

class Query():

    def __init__(self, database: str, table: str):
        self.c = sqlite3.connect(database).cursor()
        self.table = table

    def validate_parameter(self, parameter: str):
        ''' Sqlite3 uses its own parameters to make a query,
            but it does not allow to parameterize table argument.
            Thats why in this code is used f'String with string validation,
            witch secure before SQL Injection.'''
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

    def get_end_semaphore_list(self, start_semaphore: str):
        self.validate_parameter(start_semaphore)
        query = f"SELECT semafor_koncowy FROM {self.table} "\
            f"WHERE semafor_poczatkowy = '{start_semaphore}'"
        return [i for i in self.c.execute(query)]

