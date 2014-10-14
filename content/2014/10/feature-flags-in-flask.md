---
title: Feature Flags in Flask
date: 14.10.2014, 05:28
author_image: iromli.jpeg
---

__Headups: It's worth noting that although this post is about feature flags in Flask, you may find something useful
that inspires you ... hopefully.__

![flag](/img/2014/10/iwojima-lego.jpg){: class="img-thumbnail"}

There's a time when we have one or more unfinished features,
but we need to push our code into production.
Depends on our usecase, a [feature branch][feature-branch]
approach may work best for us.
But there's an alternative called __feature flag__ (also known as [feature toggle][feature-toggle]).
The latter approach keeps us away from __merging complexity__ introduced by the former,
especially if we have a long-running release cycle.

## State is Our Friend

The main idea of feature flag is to enable/disable particular features of our app simply by toggling
a state tied to each feature we want to expose/unexpose.
These states might be stored in and loaded from database, configuration file, etc.

A simple example of feature flag implementation is to enable/disable, let's say a secret page in our web app.

First things first, store the state elsewhere (database, config file, etc) as unfinished feature.
When a request hits the secret page, checks the state of that feature, then bail out — since it's an unfinished feature.
![disabled state](/img/2014/10/state-disabled.png){: class="img-thumbnail"}

Now, whenever we want to expose the secret page, simply change the state as finished.
Make sure the page is enabled when request comes in.

![enabled state](/img/2014/10/state-enabled.png){: class="img-thumbnail"}

By mangling the state, we can keep focus on writing code without worrying unfinished features got leaked to the world — unless we accidentally expose the features though.

## Flask-FeatureFlags

As I work primarily in [Flask][] nowadays,
I've found that [Flask-FeatureFlags][] extension gives me everything I need (for now),
and it's relatively easy to use.

Things to remember about FeatureFlags:

* By default, the extension loads states from app's config; most of the time it will be a Python module.
* By default, the extension uses ``dict`` with a specific format, e.g. `FEATURE_FLAGS = {"any_feature_name": True}`.
* The extension has [contrib][featureflags-contrib] modules, including interface to load states from database and [inline][featureflags-inline] string format.

### Working with Inline Format

Since I rarely using database to store configuration, I choose inline format introduced since `0.6-dev` version and it's not available at PyPI yet;
hence to install the bleeding edge version, we need to pull it from GitHub.

```sh
# install bleeding edge version of Flask-FeatureFlags
pip install -e git+https://github.com/trustrachel/Flask-FeatureFlags@02fe552ea907d9f2da271e191a9e7c5f4ff21a12#egg=Flask_FeatureFlags-master
```

One notable difference with default format is, instead of specifying features in ``dict``,
inline format recognizes the features in plain string with ``FEATURE_FLAGS_X`` format, where ``X`` is the actual feature name — all in uppercase.

```python
# default format
FEATURE_FLAGS = {
    "secret_page": True,
    "another_secret_page": False,
}

# inline format
FEATURE_FLAGS_SECRET_PAGE = True
FEATURE_FLAGS_ANOTHER_SECRET_PAGE = False
```

The disadvantage of this inline format is we have more characters to type.
But, by specifying feature using inline format, it plays nicely with [Flask-AppConfig][].
This means I can enable/disable feature using environment variable exported from command line,
as Flask-AppConfig follows the [The Twelve-Factor App][12factorapp] config manifesto.


To install Flask-AppConfig, simply use `pip` from a shell:

```sh
pip install flask-appconfig
```

Once Flask-AppConfig is configured properly, enabling/disabling a feature is simply typing it from command line.
Remember the `FEATURE_FLAGS_ANOTHER_SECRET_PAGE` line above?

Let's enable another secret page feature from a shell:

```sh
# set the value as Python truth-y
# notice the prefix before FEATURE_FLAGS_ANOTHER_SECRET_PAGE?
# it's convention used by Flask-AppConfig,
# and it doesnt' have to be APP though
APP_FEATURE_FLAGS_ANOTHER_SECRET_PAGE=1
```

In the last section of this post, I will give you snippet to implement the "secret page" example above using Flask-FeatureFlags and Flask-AppConfig.

### Flag 'em Run 'em

Given the "secret page" example above, let's implement it in a Flask app.
Don't forget to install Flask-FeatureFlags and Flask-AppConfig first.

```python
# app.py
import flask
import flask_featureflags as feature
from flask.ext.appconfig import AppConfig
from flask_featureflags.contrib.inline import InlineFeatureFlag

FEATURE_FLAGS_SECRET_PAGE = False

app = flask.Flask(__name__)

# As we're passing `__name__` when creating Flask app,
# it means our `app.name` equals to "app".
# Flask-AppConfig will recognize any `APP_*` env variable.
# If we need to change the prefix, set `app.name`
# into something else, before initializing the extension.

# Loads default config from current module
appconfig = AppConfig(app, default_settings=__name__)

flags = feature.FeatureFlag(app)
flags.add_handler(InlineFeatureFlag())


@app.route("/")
def index():
    return "Homepage"


@app.route("/secret")
@feature.is_active_feature("SECRET_PAGE", redirect_to="/")
def secret_page():
    return "Secret Page"

app.run()
```

To test whether "secret page" is disabled, simply run:

```sh
python app.py
```

To enable "secret page" from a shell, run:

```sh
APP_FEATURE_FLAGS_SECRET_PAGE=1 python app.py
```

It's quite simple isn't it?


[feature-branch]: http://martinfowler.com/bliki/FeatureBranch.html
[feature-toggle]: http://martinfowler.com/bliki/FeatureToggle.html
[Flask]: http://flask.pocoo.org/
[Flask-FeatureFlags]: https://github.com/trustrachel/Flask-FeatureFlags
[featureflags-contrib]: https://flask-featureflags.readthedocs.org/en/latest/contrib.html
[featureflags-inline]: https://github.com/trustrachel/Flask-FeatureFlags/blob/73a960f62e4f504452538e0a5f56ace08ea68390/CHANGES.rst#051-october-13-2014
[Flask-AppConfig]: https://pypi.python.org/pypi/flask-appconfig
[12factorapp]: http://12factor.net/config
