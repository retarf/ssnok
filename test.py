import unittest
import unittest.mock
from query import Query, QueryError, SOURCE_DB, TABLE
#from route import Route, RouteError
from mileage import Mileage, Semaphore

class TestQueryMethods(unittest.TestCase):

    def setUp(self):
        self.query = Query(SOURCE_DB, TABLE)

    def test_validate_parameter(self):
        wrong_string = "test_$tring"
        right_string = "Test_String_22"

        self.query.validate_parameter(right_string)
        self.assertRaises(QueryError, self.query.validate_parameter, wrong_string)

    def test_set_table(self):
        table = 'test_table'
        self.query.table = table
        result = self.query.table
        self.assertEqual(table, result)

    def test_get_end_semaphore_list(self):
        result = self.query.get_end_semaphore_list('semafor_A')
        self.assertEqual([], result)

    def test_find_mileage_without_arguments(self):
        self.assertRaises(QueryError, self.query.find_mileage)

    def test_find_mileage_with_too_many_arguments(self):
        kwargs={"mileage_id": 10, "start": "semafor_10"}
        self.assertRaises(QueryError, self.query.find_mileage, **kwargs)

    def test_find_milage_with_one_argument(self):
        asserted = [(10, 'SEMAFOR_0', 'SEMAFOR_72')]

        result = self.query.find_mileage(mileage_id=10)
        self.assertEqual(asserted, result)

        result = self.query.find_mileage(start='SEMAFOR_0')
        self.assertEqual(asserted, result)

        result = self.query.find_mileage(end='SEMAFOR_72')
        self.assertEqual(asserted, result)

class TestRouteMethods(unittest.TestCase):

    def setUp(self):
        self.first = (1, 'SEMAFOR_1', 'SEMAFOR_2')
        self.second = (2, 'SEMAFOR_2', 'SEMAFOR_3')
        self.third = (3, 'SEMAFOR_3', 'SEMAFOR_4')
        self.fourth= (4, 'SEMAFOR_4', 'SEMAFOR_5')
        self.fifth = (5, 'SEMAFOR_5', 'SEMAFOR_6')
        self.all = [self.first, self.second, self.third, self.fourth,
            self.fifth]

    def test_create_route_whit_too_many_arguments(self):
        self.assertRaises(RouteError, Route, self.all)

    def test_append_too_many_arguments_to_route(self):
        r = Route()
        for i in self.all[:4]:
            r.append(i)
        self.assertRaises(RouteError, r.append, self.fifth)

    def test_append_wrong_mileage_to_route(self):
        r = Route()
        r.append(self.first)
        self.assertRaises(RouteError, r.append, self.third)

    def test_append_wrong_mileage_to_route(self):
        r = Route()
        r.append(self.first)
        self.assertRaises(RouteError, r.append, self.third)

class TestMileageMethods(unittest.TestCase):

    def setUp(self):
        self.data = (1, 'SEMAFOR_1', 'SEMAFOR_2')
        self.wrong_tuple = (1, 'SEMAFOR_1', 'SEMAFOR_2', 'test')
        self.wrong_id = ('1', 'SEMAFOR_1', 'SEMAFOR_2')
        self.wrong_start = (1, 'semafor_1', 'SEMAFOR_2')
        self.wrong_end = (1, 'SEMAFOR_1', 'semafor_2')

    def test_create_mileage_should_succed(self):
        mileage = Mileage(self.data)
        self.assertIsInstance(mileage, Mileage)

    def test_create_mileage_with_wrong_tuple_should_fail(self):
        self.assertRaises(MileageError, Mileage, self.wrong_tuple)

    def test_create_mileage_with_wrong_id_should_fail(self):
        self.assertRaises(MileageError, Mileage, self.wrong_id)

    def test_create_mileage_with_wrong_start_should_fail(self):
        self.assertRaises(MileageError, Mileage, self.wrong_start)

    def test_create_mileage_with_wrong_end_should_fail(self):
        self.assertRaises(MileageError, Mileage, self.wrong_end)

test_query = [(1, 'SEMAFOR_1', 'SEMAFOR_2'),
              (2, 'SEMAFOR_2', 'SEMAFOR_3'),
              (3, 'SEMAFOR_3', 'SEMAFOR_4'),
              (6, 'SEMAFOR_3', 'SEMAFOR_7'),
              (7, 'SEMAFOR_7', 'SEMAFOR_9'),
              (8, 'SEMAFOR_7', 'SEMAFOR_10'),
              (9, 'SEMAFOR_9', 'SEMAFOR_11'),
              (10,'SEMAFOR_11', 'SEMAFOR_12'),
              (4, 'SEMAFOR_4', 'SEMAFOR_5'),
              (5, 'SEMAFOR_5', 'SEMAFOR_6')]

test_m_query = [Mileage(i) for i in test_query]

import sqlite3

class TestQuery():

    def __init__(self):
        self.test_db = 'db/test_db.db'
        self.conn = sqlite3.connect(self.test_db)
        self.table = 'przebiegi'

    def create_database(self):
        create_query = '''CREATE TABLE IF NOT EXISTS przebiegi (
                            id integer PRIMARY KEY,
                            semafor_poczatkowy text NOT NULL,
                            semafor_koncowy text NOT NULL
                            );'''

        self.conn.execute(create_query)

    def get_column_names(self):
        query = f"PRAGMA table_info({self.table});"
        return self.conn.execute(query).fetchall()

class TestSemaphoreMethods(unittest.TestCase):

    def setUp(self):
        self.name = 'SEMAPHORE_1'
        self.sx = "SX"
        self.s1 = "S1"

    def test_set_semaphore_state_should_succed(self):
        semaphore = Semaphore(self.name)
        semaphore.state = self.sx
        self.assertEqual(self.sx, semaphore.state)
        semaphore.state = self.s1
        self.assertEqual(self.s1, semaphore.state)

    def test_set_semaphore_state_should_succed(self):
        semaphore = Semaphore(self.name)
        with self.assertRaises(Exception):
            semaphore.state = "SA"

if __name__ == '__main__':
    unittest.main()
