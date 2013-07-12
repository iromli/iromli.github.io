Groovematic
===========

The source code behind my [personal website](http://groovematic.com/).
It's [unlicensed](http://unlicense.org/) anyway.

Requirements
------------

Python libraries:

    $ pip install -r requirements.txt

Hacking
-------

Compile and serve the content at `http://localhost:8000/`:

    $ acrylamid autocompile

Deploy:

    $ rm -rf output
    $ acrylamid compile
    $ git checkout gh-pages
    $ rsync -rvc --delete-after --exclude=CNAME --exclude=.git* output/ .
    $ git push origin gh-pages

Todo
----

* Robust deployment
