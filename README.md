# routex

routex is a simple routing module which have a clear api.

*Write a web framework for myself step-01 : routex.*

**1.route obj**

``` bash
>>> from routex import Route
>>> r = Route("/<name:str>/<age:int>", lambda:"hello")
>>> r()
'hello'
>>> r.match("/Kobe/24")
True
>>> r.match("/James/Laker")
False
```

**2.router obj**

``` bash
>>> from routex import Route, Router
>>> rt = Router()
>>> rt.add(Route("/<name:str>/<heigth:float>/<age:int>", lambda: 1))
>>> rt.add(Route("/person/12", lambda: 2))
>>> rt.add(Route("/", lambda: 3))
>>> rt.match("/")
<Route pattern='/'>
>>> rt.match("/kobe")
>>> rt.match("/kobe/198.12/24")
<Route pattern='/<name:str>/<heigth:float>/<age:int>'>
>>> rt.match("/person/12")
<Route pattern='/person/12'>
```

**define a url filter**

``` python
from routex import url_param_filter

@url_param_filter("good")
def good_filter(s: str):
	return s == "good"

# your route can define like this

r = Route("/<how:good>", lambda:22)
r.match("/bad") #False
r.match("/good") #True
```
