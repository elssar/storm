#!/usr/bin/python

import datetime


class Model(object):

    FILTER_MAP = {
        "eq": "=",
        "neq": "!=",
        "lt": "<",
        "lte": "<=",
        "gt": ">",
        "gte": ">=",
    }

    def __init__(self, table):
        self.table = table

    def _clean_value(self, value):
        if isinstance(value, (str, unicode)):
            return "\"{0}\"".format(value)
        elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
            return "\"{0}\"".format(value)
        elif isinstance(value, (int, float)):
            return value

    def filter(self, **filters):
        query = "SELECT * FROM {0}".format(self.table)
        filter_clauses = []
        for key, value in filters.iteritems():
            cleaned_value = self._clean_value(value)
            filter_parts = key.split("__")
            if len(filter_parts) > 1:
                operator = self.FILTER_MAP.get(filter_parts[-1])
                if not operator:
                    operator = "="
                else:
                    filter_parts = filter_parts[:-1]
            else:
                operator = "="

            filter_clauses.append("{0}{1}{2}".format("__".join(filter_parts),
                                                     operator, cleaned_value))

        filter_string = " AND ".join(filter_clauses)
        if filter_string:
            query = "{0} WHERE {1}".format(query, filter_string)

        return "{0};".format(query)
