---
title: Python: When The Two Become One
date: 09.08.2014, 14:41
author_image: iromli.jpeg
---

## The Gap Between 2 Python Worlds

Most of the time, any newcomer to Python programming language probably will ask should they learn Python 2 or 3.
Python core developers — most of the time — will lead the newcomers to enter into Python 3 world.
On the other hand, a few of Python heroes who rant about several things in Python 3,
likely will tell newcomers to stick with Python 2 for now, until the transition process is smoother.

From my point of view, I truly agree on how we should moving forward.
Despite of Python 2 is still alive and kickin', the current development is heavily-geared toward Python 3,
because it's the future!

Unfortunately, reality bites for sure. There are many reasons why people still working on Python 2 codebase:

* Unable to find a replacement for third-party library that doesn't have Python 3 support yet.
* Huge/complex legacy codebase — rewriting the code to use Python 3 is too risky for the business.
* Worrying too much about changes made in Python 3.
* And so on ...

Now, as a pragmatic developer, I know the feeling of having those unpleasant moments.
But as a person who loves Python, I want to see this language evolves.
Let's not making war about Python 2 vs 3 anymore. Let's us minimize the gap instead,
by starting to learn how to love Python 3 while still working on Python 2 codebase.

Fair enough?

## One Codebase to Rule 'em All!

I've started to write code that supports both Python 2 and 3 since 6 months ago,
so when Python 3 is the only Python that lives in real-world,
the transition to use the new codebase is smoother (hopefully).
Hence the rest of this blog post is simply opinionated based on my experience.

### 1 - Checks for New/Changed/Removed Stuff

Python 3 introduces new stuff, removes old stuff, and changes several import names.
I would suggest to read [What's New in Python 3][] page and [Nick Coghlan's Python 3 Notes][] first.

[Nick Coghlan's Python 3 Notes]: http://python-notes.curiousefficiency.org/en/latest/python3/index.html
[What's New in Python 3]: https://docs.python.org/3/whatsnew/3.0.html

### 2 - Checks for Dependencies

As I've mentioned before, third-party library might blocked our transition to Python 3 codebase.
Luckily, there's a neat tool called [caniusepython3][].
It checks whether third-party dependencies required by our code block the transition,
but beware of their false alarm.
If we see a warning about unsupported library, please double check by trying the library and see how it goes.

[caniusepython3]: https://caniusepython3.com

### 3 - Use Compatibility Helper

Compatibility helper is code that ensures our code runs in Python 2 and 3.
Don't worry about this, the author of third-party library we're using in our code
might have write it down for us.
If it's not, we can use general-purpose helper e.g. [six][] or [python-future][].

[six]: https://pythonhosted.org/six/
[python-future]: http://python-future.org/

### 4 - Automated Testcases

I'm not a testcases fanboy/purist, but sometime writing automated testcases will help us speedup the development,
remove tedious steps, and so on.
Spend our time to write testcases, please.
Tools like unittest, [pytest][], and [nose][] will save our day; choose whatever fits our taste.

[pytest]: http://pytest.org/
[nose]: https://nose.readthedocs.org/

### 5 - Python Environment Management

Since we're writing code that suppose to run in Python 2 and 3 — which require their own environments,
automating test environment management is important.
Well, [tox][] and [pyenv][] is a neat combination we can rely on.

[tox]: https://testrun.org/tox/
[pyenv]: https://github.com/yyuu/pyenv

## When The Two Become One

Learning how to love Python 3 while dealing with Python 2 codebase is not that simple.
It's easier said than done, but practice makes perfect isn't it?

Let ask ourselves, when Python 3 completely deprecates Python 2 in real-world,
how much time we would have to spend to learn the new stuff?
Why don't we start from now?

If I don't convince you enough, perhaps [Kenneth Reitz's talk][] will move you on?

[Kenneth Reitz's talk]: http://www.youtube.com/watch?v=skYBOXE02OQ
