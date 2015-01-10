#!/usr/bin/python


from filter_clause import FilterClause


class Model(object):

    @classmethod
    def filter(cls, **filters):
        query = "SELECT * FROM {0}".format(cls.table)
        filter_clauses = []
        for key, value in filters.iteritems():
            filter_clause = FilterClause(key, value)

            filter_clauses.append(filter_clause.to_query())

        filter_string = " AND ".join(filter_clauses)
        if filter_string:
            query = "{0} WHERE {1}".format(query, filter_string)

        return "{0};".format(query)
