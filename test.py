import unittest
from routex import Route, RouteParseException, RoutePatternException


class TestRoute(unittest.TestCase):
    def test_route_create(self):
        r = Route("/", lambda: "hello")
        self.assertEqual(r.pattern, "/")
        self.assertEqual(r.callback(), "hello")

        with self.assertRaises(RouteParseException):
            r = Route("/hello?app=12", lambda: "hello")
        with self.assertRaises(RouteParseException):
            r = Route("/hello#jks", lambda: "world")
        with self.assertRaises(RouteParseException):
            r = Route("http://www.baidu.com/", lambda: "sorry")
        with self.assertRaises(RoutePatternException):
            r = Route("", lambda: "world")

    def test_route_match(self):
        r = Route("/", lambda: "hello")
        self.assertFalse(r.match(""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
