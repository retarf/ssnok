import unittest
import unittest.mock
from query import Query, QueryError, SOURCE_DB, TABLE

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

if __name__ == '__main__':
    unittest.main()
