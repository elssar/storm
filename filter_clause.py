import datetime


class FilterClause(object):

    FILTER_MAP = {
        "eq": "=",
        "neq": "!=",
        "lt": "<",
        "lte": "<=",
        "gt": ">",
        "gte": ">=",
    }

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def __and__(self, obj):
        if isinstance(obj, FilterClause):
            return "{0} AND {1}".format(self.to_query(), obj.to_query())
        elif isinstance(obj, (str, unicode)):
            return "{0} AND {1}".format(self.to_query(), obj)

        raise TypeError

    def __or__(self, obj):
        if isinstance(obj, FilterClause):
            return "{0} OR {1}".format(self.to_query(), obj.to_query())

        elif isinstance(obj, (str, unicode)):
            return "{0} OR {1}".format(self.to_query(), obj)

        raise TypeError

    def _clean_value(cls, value):
        if isinstance(value, (str, unicode)):
            return "\"{0}\"".format(value)
        elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
            return "\"{0}\"".format(value)
        elif isinstance(value, (int, float)):
            return value

    def to_query(self):
        filter_key = self.key.split("__")
        if len(filter_key) > 1:
            filter_operator = self.FILTER_MAP.get(filter_key[-1])
            if not filter_operator:
                filter_operator = "="
            else:
                filter_key = filter_key[:-1]
        else:
            filter_operator = "="

        return u'{}{}{}'.format(filter_key[0], filter_operator,
                                self._clean_value(self.value))
