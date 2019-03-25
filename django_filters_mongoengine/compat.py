__all__ = ("QUERY_TERMS",)

# Valid query types (a set is used for speedy lookups). These are (currently)
# considered SQL-specific; other storage systems may choose to use different
# lookup types.
QUERY_TERMS = {
    "exact",
    "iexact",
    "contains",
    "icontains",
    "gt",
    "gte",
    "lt",
    "lte",
    "in",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "range",
    "year",
    "month",
    "day",
    "week_day",
    "hour",
    "minute",
    "second",
    "isnull",
    "search",
    "regex",
    "iregex",
}
