# routex

Write a web framework step-01 for myself: routex.

routex is a simple routing module which have a clear api.

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
