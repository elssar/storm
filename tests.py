#!/usr/bin/python

import unittest

from storm import Model
from filter_clause import FilterClause


Q = FilterClause


class TestModel(Model):
    table = "test"


class StormTest(unittest.TestCase):

    def test_returns_query_for_eqality(self):
        query = TestModel.filter(name='foo')

        expected_query = 'SELECT * FROM test WHERE name="foo";'
        assert query == expected_query

    def test_returns_query_for_equality_with_and(self):
        query = TestModel.filter(name='foo', age=24)

        expected_query = 'SELECT * FROM test WHERE age=24 AND name="foo";'
        assert query == expected_query

    def test_returns_query_for_ineqality(self):
        query = TestModel.filter(name__neq='foo')

        expected_query = 'SELECT * FROM test WHERE name!="foo";'
        assert query == expected_query 

    def test_returns_query_for_less_than(self):
        query = TestModel.filter(age__lt=25)

        expected_query = 'SELECT * FROM test WHERE age<25;'
        assert query == expected_query 

    def test_returns_query_for_greater_than(self):
        query = TestModel.filter(age__gt=25)

        expected_query = 'SELECT * FROM test WHERE age>25;'
        assert query == expected_query 

    def test_complex_query(self):

        query = TestModel.filter(Q(key="age", value=25) &
                                 Q(key="name", value="Akshay") |
                                 Q(key="name", value="Nitish") |
                                 Q(key="company", value="Red Panda"))

        expected_query = 'SELECT * FROM test WHERE age=25 AND name="Akshay" OR name="Nitish" OR company="Red Panda";'
        assert query == expected_query


class FilterClauseTest(unittest.TestCase):
    def test_should_get_query(self):
        key = 'name'
        clause = FilterClause(key, 'foo')

        assert clause.to_query() == '{}={}'.format(key, '"foo"')

    def test_should_create_from_key_and_value(self):

        query = FilterClause('name__eq', 'foo').to_query()

        assert query == 'name="foo"'
