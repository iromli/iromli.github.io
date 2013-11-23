---
title: Tornado, Lessons Learned
date: 04.03.2013, 04:19
---

## Back In The Days

Last year, during [SixReps][sixreps] days, me and Tino ([@kusut][_kusut])
worked on and maintained a project built on top of [Tornado][tornado].
The project itself is a web service that accepts 3rd-party apps request
and serves the response through HTTP.
We used MySQL as primary datasource, [Redis][redis] for caches and queues,
and Amazon S3 to store uploaded images.
We were happy enough to see that our stack is running well for our usecase.

__FYI__, both of us aren't worked on that project any longer.

[sixreps]: http://www.sixreps.com
[_kusut]: http://twitter.com/kusut
[tornado]: http://tornadoweb.org/
[redis]: http://redis.io/

## For Your Consideration

I'm not going to go deeper about our implementation nor Tornado API itself
(i'm not a Tornado guru yet, perhaps someday in future?).
Instead, i will share lessons learned after using this nifty framework.
The idea is to notify newcomers about gotchas they might encounter
and tradeoffs they should aware of when using Tornado.

Basically, before starting any serious work using Tornado,
you should ask yourself these questions:

1. Does your app need to be synchronous/asynchronous?
2. Do you comfortable with callback-style programming?

## Being Synchronous (Is Mostly Fine)

If your app doesn't care about being asynchronous, you can start writing code
immediately.
You might wondering why bother yourself using something that written for
asynchronous, but you don't even care about asynchronous at all?

1.  Tornado is not a full-stack framework. It's simple, well-written, and well-documented.
    By reading the sourcecode itself, you'll understand how it works ... eventually.
2.  Tornado has its own web framework (much like [web.py][webpy]).
3.  Tornado has its own templating language (quite similar to [Jinja][jinja]).
4.  Tornado has its own web server.
5.  The most important things, you can use (almost?) any Python library, even if it's not written specifically for Tornado.

[jinja]: http://jinja.pocoo.org/
[webpy]: http://webpy.org/

Let me show you snippets to illustrate point 2 - 4. First things first, create
`app.py`:

    #!python
    import tornado.web          # the Tornado web framework
    import tornado.httpserver   # the Tornado web server
    import tornado.ioloop       # the Tornado event-loop

    # handles incoming request, this is the C part in MVC
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            # renders the Tornado template
            self.render('homepage.html', user='John Doe')

    # prepares the application
    app = tornado.web.Application([
            (r"/", MainHandler),
        ], debug=True, template_path='templates')

    if __name__ == '__main__':
        # prepares the web server
        srv = tornado.httpserver.HTTPServer(app, xheaders=True)

        # listens incoming request on port 8000
        srv.bind(8000, '')

        # starts the server using 1 process
        # unless you know what you're doing, always set to 1
        srv.start(1)

        # runs all the things
        tornado.ioloop.IOLoop.instance().start()

Before running the app, make sure you have `homepage.html` template, located
under `templates` directory:

    #!html
    <h1>Greeting from Tornado</h1>
    <p>Hello, {{ user }}</p>

Run the app by typing `python app.py` in your console, and go to `http://localhost:8000/`.
Now you already have a synchronous app built on top of Tornado.
Pretty straight-forward isn't it?

So, what's the _tradeoff of being synchronous_?
You'll lose the power of Tornado event-loop itself, of course.
Some users claimed they use a combination of [Django][django]/[Flask][flask] and Tornado.
It's true that Tornado has a WSGI-compatible web server,
but you can't expect your app to go asynchronously out-of-the-box
by simply running it behind the Tornado web server.

[django]: https://www.djangoproject.com/
[flask]: http://flask.pocoo.org

## Going Asynchronous (Or How To Not Blocking The IOLoop)

I already mentioned `tornado.ioloop.IOLoop` on previous section.
Basically, IOLoop is a Tornado binding to the underlying event-loop
(`epoll` on Linux and `kqueue` on BSD).
I don't know about Windows support, but there's a project
called [tornado-pyuv][tornado-pyuv] that utilizes `libuv` to provide event-loop that runs
on all platforms.

[tornado-pyuv]: https://github.com/saghul/tornado-pyuv

You have to be very careful when writing asynchronous app using Tornado.
Your simple code that uses `stdlib` callables or 3rd-party libraries might blocking the IOLoop.
How do we know IOLoop is blocked?
It's hard, but what i was doing back in the days is testing against 2 incoming requests.
If a request must wait for another request to finish, then IOLoop is blocked.

To illustrate `stdlib` callable which blocks IOLoop:

    #!python
    import time

    import tornado.httpclient
    import tornado.httpserver
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
            client = tornado.httpclient.AsyncHTTPClient()
            client.fetch('http://groovematic.com/', callback=self._on_finish)

        def _on_finish(self, response):
            self.write(str(response.code))
            self.finish()

    class SleepHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
            time.sleep(3)           # time.sleep is blocking IOLoop, dooh
            self.write('hello')
            self.finish()

    app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/t", SleepHandler),
        ], debug=True)

    if __name__ == '__main__':
        srv = tornado.httpserver.HTTPServer(app, xheaders=True)
        srv.bind(8000, '')
        srv.start(1)
        tornado.ioloop.IOLoop.instance().start()

Open up your console, type `curl http://localhost:8000/t`.
In separate window, type `curl http://localhost:8000/`.
You'll see that `/` have to wait `/t` to finish its request-response cyle
within 3 seconds.
Fortunately, there's Tornado equivalent to `time.sleep`.
Please have a look at `IOLoop.add_timeout` API.

To be honest, 3rd-party libraries written specifically for Tornado is not as
much as, let say, Django.
You have to dig into [Tornado wiki](https://github.com/facebook/tornado/wiki/Links),
[GitHub](https://github.com/), [Bitbucket](https://bitbucket.org/),
[Tornado gist](http://tornadogists.org/), or somewhere else
(IRC/mailing list/search engine) to find what you're looking for.

If for some reasons you must use blocking library, you have options to run the
blocking execution in separate process,
either using [threading][example1], [multiprocessing][example2],
or [queue][example3].
The implementation may vary, but they share a same concept:

1. Wrap the blocking execution and give the control back to IOLoop immediately.
2. Run the blocking execution in separate process.
3. Notify and/or send the result of blocking execution back to IOLoop.

So, what's the _tradeoff of going asynchronous_?
Once you're using blocking library, IOLoop is blocked.
Depending on your usecase, it might be bad for your business.
That's a price to pay.

[example1]: http://tornadogists.org/2894704/
[example2]: http://tornadogists.org/2185380/
[example3]: http://tornadogists.org/3849257/

## Callbacks Spaghetti? Fear No More!

To me, the most tricky part of Tornado (in general) and IOLoop (especially),
is dealing with callbacks.
If you came from JavaScript or other programming languages emphasizing
callback-style programming, you'll know what callback is.

Lets take a look an example below:

    #!python
    import tornado.httpclient
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
            client = tornado.httpclient.AsyncHTTPClient()
            client.fetch('http://groovematic.com/', callback=self._on_finish)

        def _on_finish(self, response):
            self.write(str(response.code))
            self.finish()

Nothing's wrong isn't it? But what if you want to get the result directly
instead of using callback?
You shouldn't worry that much, there's `tornado.gen` module which simplifies things.
It helps you write a non-callback-style code.

    #!python
    import tornado.gen
    import tornado.httpclient
    import tornado.web

    class MainHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        @tornado.gen.engine
        def get(self):
            client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(client.fetch, 'http://groovematic.com/')
            self.write(str(response.code))
            self.finish()

Yay, it looks better now. Say goodbye to callbacks spaghetti then.

## Morals Of The Story

1. You don't care about asynchronous but still wanna use Tornado? Just do it.
2. You have things for asynchronous and wanna use Tornado? Do it carefully.
3. You don't like callbacks when writing Tornado-based app? Use helpers.

__PS__: Eventually you'll get this Tornado thingy sooner or later.
You might roll your own IOLoop-compatible library someday (i wrote [dusky](https://github.com/iromli/dusky)).
It's always fun to learn something new. Trust me, i've been there, done that.