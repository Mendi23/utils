from typing import Any, Callable, Dict, List, Union

_exists: Callable[[str], Dict] = lambda field_name: {"exists": {"field": field_name}}
_not: Callable[[Dict], Union[Dict, List]] = lambda cond: {"bool": {"must_not": cond}}
_and: Callable[
    [List[Dict]],
    Dict] = lambda conds: {"bool": {"must": conds}} if len(conds) > 1 else conds[0]
_or: Callable[
    [List[Dict]],
    Dict] = lambda conds: {"bool": {"should": conds}} if len(conds) > 1 else conds[0]
_equal: Callable[[str, Any], Dict] = lambda field, value: {"term": {field: value}}
_any: Callable[[str, List[Any]], Dict] = lambda field, values: {"terms":
    {field: values}} if len(values) > 1 else _equal(field, values[0])
_query: Callable[[Dict], Dict] = lambda query: {"query": query}
_nested: Callable[[str, Dict],
                  Dict] = lambda path, query: {"nested": {"path": path, **query}}