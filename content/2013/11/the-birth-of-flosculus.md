---
title: The Birth of Flosculus
date: 23.11.2013, 05:18
author_image: iromli.jpeg
---

## A Call For Help

Few days ago, i tweeted this:

![CPU-blown](/img/2013/11/cpu-blown.png){: class="thumbnail"}

If you notice, the top 2 commands show a huge difference between
CPU usage consumed by Ruby and Python programs — the former is a
[Fluentd][fluentd]-based script that collects [nginx][nginx] access log,
parses each line, and sends the data to another Fluentd instance
(in remote server); while the latter is a [socket.io][socket.io]
server built on top of [gevent-socketio][gevent-socketio] —
in AWS EC2 micro instance.

I was wondering what went wrong?
Hence i looked up to the official [AWS EC2 documentation][ec2]
to find any hint, and stumbled upon a line:

> Limit the number of recurring processes that use CPU time (for example, cron jobs, daemons)

That's strange!! Both are daemonized long-running programs, but why the Ruby script blown the CPU?
Do i need to have a bigger box for a small service
and convince my employer to spend more money?

[beautiplan]: https://www.beautiplan.com/
[gevent-socketio]: https://github.com/abourget/gevent-socketio
[fluentd]: http://fluentd.org/
[nginx]: http://nginx.org/
[socket.io]: http://socket.io/
[ec2]: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts_micro_instances.html#when-instance-uses-allotted-resources

## First Attempt: Becoming A Rubyist

That day, i was reading the sourcecode trying to figure out
how Fluentd works internally. __And i failed!!__

As you might have known, i know nothing about Ruby nowadays — my Ruby days were long gone.
Please don't get me wrong, Ruby is a sexy programming language.
But you know what, not all people able to deal with the _hottie_ for a long-term relationship.

![nosebleed](/img/2013/11/nosebleed-anime.jpg){: class="thumbnail"}

## Second Attempt: Keep Calm & Move On

At the same day, i suddenly remembered about a Python library called [Beaver][beaver].
From its repository page, Beaver is best described as:

> python daemon that munches on logs and sends their contents to logstash

Obviously, Beaver acts as a [Logstash][logstash] input plugin.
Well, i can haz Beaver for Fluentd?

[beaver]: https://github.com/josegonzalez/beaver
[logstash]: http://logstash.net/

### Looking At The Big Picture

So i sat down and read the internal documentation on how [Beautiplan][beautiplan]
infrastructure are made of — especially the logging files management section.
Anyway, here's the schema with a little detail for each component:

![schema](/img/2013/11/schema.png){: class="thumbnail"}

1.  #### forwarder

    _forwarder_ is a daemonized program. Its main job is tailing a rotated log file,
    parse each line, and send the result to _aggregator_ elsewhere.
    Just imagine a `tail -F scarry.log` command with steroid.
    Fluentd, Beaver, or your own script fits the job, as long as it knows
    how to speak to _aggregator_.

2.  #### aggregator

    Actually _aggregator_ is the first-class citizen here.
    Everything is setup to match its behavior.
    Its job is to receive incoming data — usually a JSON — do some works,
    and send the result elsewhere, either a simple _stdout_ or remote _datastore_.
    Fluentd, Logstash, or even [Heka][heka] will do the job for you.

3.  #### datastore

    The _datastore_ stores (dooh) the timeseries data extracted from a log.
    It's [ElasticSearch][elasticsearch] by the way. Other datastores might work.

4.  #### frontend

    Remember the old days when you have to stare hundred lines of a log file (bad)
    or doing shell command and pipeline magic (better) to know what's really
    going on in your production-ready application?
    Enter [Kibana][old_kibana] or [Kibana 3][new_kibana] then!
    I think you'll like this web-based log visualization app.

Given the schema above, i realized that i need to replace _forwarder_ with
Beaver-like library. After all, the box where current _forwarder_ program lives
right now, is a server where it has plenty of Python-based scripts there.
So i though, let's add yet another Python script.

[beautiplan]: http://www.beautiplan.com/
[heka]: https://github.com/mozilla-services/heka
[elasticsearch]: http://elasticsearch.org/
[old_kibana]: http://rashidkpc.github.io/Kibana/
[new_kibana]: http://www.elasticsearch.org/overview/kibana/

## Current Status: Flosculus in Action

At its core, Beaver uses [this script][script] (MIT-licensed).
So i took down that one, combined with [Python binding for Fluentd][fluent-logger],
did some modification, and voila ... it's [Flosculus][flosculus].
Flosculus is very young and definetely will need lots of enhancements.
But it's already running in production though.

Yes, i know some of you might said, _"Dont reinvent the wheel"_.
But what if the wheels aren't exactly what i need?

![bicycle](/img/2013/11/bicycle.jpg){: class="thumbnail"}

In the end, Flosculus is my attempt to create something like Beaver or Fluentd `in_tail` plugin.
I wanna see it grows (or likely dies prematurely). The future is far beyond.

[script]: http://code.activestate.com/recipes/577968-log-watcher-tail-f-log/
[fluent-logger]: https://github.com/fluent/fluent-logger-python
[flosculus]: https://github.com/iromli/flosculus
