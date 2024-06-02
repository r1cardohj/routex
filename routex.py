from typing import Callable, Optional, List
from itertools import zip_longest
from urllib.parse import urlparse
from collections.abc import Iterable
import re


###### some Exception ##########
class RouteException(Exception):
    pass


class RouteParseException(RouteException):
    pass


class RoutePatternException(RouteException):
    pass


class URLException(Exception):
    pass


class URLFilterException(URLException):
    pass


class URLFilterUndefineException(URLFilterException):
    pass


# url param filter is for check url content
_url_param_filters = {}


def url_param_filter(filter_name: str):
    """a wrapper for create a url_param_filter,
    simple and clear.

    ex::
    >>> @url_param_filter("good")
    ... def my_good_filter(s: str):
            return s == "good"
    """

    def decorated(func: Callable[[str], bool]):
        global _url_param_filters
        _url_param_filters[filter_name] = func
        return func

    return decorated


@url_param_filter("path")
def _url_path_filter(s: str):
    # todo
    return bool(s)


@url_param_filter("int")
def _url_int_filter(s: str):
    return s.isdigit()


@url_param_filter("str")
def _url_str_filter(s: str):
    if s == "":
        return False
    try:
        str(s)
    except:
        return False
    return True


@url_param_filter("float")
def _url_float_filter(s: str):
    try:
        float(s)
    except:
        return False
    return True


##### Route and Router #####


class Route:
    """route is a item in router,
    ex::

        >>> r = Route("/", lambda: "hello world")
        >>> r()
        "hello world"
        >>> r1 = Route("/<name:str>/<age:int>", lambda: "sorry")
        >>> r1.match("/whoami/12")
        True
    """

    #: match like '<name:str>' or '<age:int>' in url path.
    ROUTE_PARAM_PATTERN = r"<([^:>]+):([^>]+)>"

    def __init__(self, pattern: str, callback: Callable[[], Iterable]) -> None:
        if pattern == "":
            raise RoutePatternException("pattern '' is vaild.")
        # check url path is ok
        if urlparse(pattern).path != pattern:
            raise RouteParseException
        self.pattern = pattern
        self.pattern_groups = pattern.split("/")

        self.callback = callback

    def match(self, url_path: str) -> bool:
        if url_path == "":
            return False
        path_groups = url_path.split("/")
        for pattern, elem in zip_longest(self.pattern_groups, path_groups):
            if pattern is None or elem is None:
                return False
            # match <{param_name:filter_name}>
            m = re.match(Route.ROUTE_PARAM_PATTERN, pattern)
            if m:
                filter_name = m.group(2)
                if filter_func := _url_param_filters.get(filter_name):
                    if not filter_func(elem):
                        return False
                else:
                    raise URLFilterUndefineException(
                        f"filter {filter_name} is undefine."
                    )
            else:
                if pattern != elem:
                    return False
        return True

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    def __repr__(self):
        return f"<Route pattern='{self.pattern}'>"


class Router:
    """
    Router is for find route by url_path.
    """

    def __init__(self) -> None:
        self.routes: List[Route] = []

    def add(self, route: Route) -> None:
        self.routes.append(route)

    def match(self, url_path: str) -> Optional[Route]:
        for route in self.routes:
            if route.match(url_path):
                return route
        return None
