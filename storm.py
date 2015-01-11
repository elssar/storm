#!/usr/bin/python


from filter_clause import FilterClause


class Model(object):

    @classmethod
    def filter(cls, *args, **kwargs):
        query = "SELECT * FROM {0} WHERE".format(cls.table)
        filter_clauses = []

        if args:
            positional_filter_string = args[0].to_query()
            query = "{0} {1}".format(query, positional_filter_string)

        for key, value in kwargs.iteritems():
            filter_clause = FilterClause(key, value)

            filter_clauses.append(filter_clause.to_query())

        filter_string = " AND ".join(filter_clauses)
        if filter_string:
            query = "{0} {1}".format(query, filter_string)

        return "{0};".format(query)
