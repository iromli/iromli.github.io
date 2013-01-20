Groovematic
===========

The source code behind my [personal website](http://groovematic.com/).
It's [unlicensed](http://unlicense.org/) anyway.

Requirements
------------

Python libraries:

* [Acrylamid](https://github.com/posativ/acrylamid)
* [Watchdog](https://github.com/gorakhargosh/watchdog)

NodeJS libraries:

* [LESS](http://lesscss.org/)

Hacking
-------

Compile and serve the content at http://localhost:8000/

    acrylamid autocompile

Use `watchdog` to monitor changes in any `.less` file.

    watchmedo shell-command \
        --patterns="*.less" \
        --recursive \
        --command="lessc -x $PWD/less/style.less > $PWD/assets/css/style.css" \
        $PWD
