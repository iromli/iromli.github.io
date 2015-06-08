# -*- encoding: utf-8 -*-
# This is your configuration file.  Please write valid python!
# See http://posativ.org/acrylamid/conf.py.html

SITENAME = "Groovematic"
WWW_ROOT = "http://groovematic.com/"

AUTHOR = "Isman Firmansyah"
EMAIL = "isman.firmansyah@gmail.com"

FILTERS = [
    "markdown+extra+codehilite(css_class=highlight, linenums=False)",
    "hyphenate",
    "h1",
]

VIEWS = {
    "/": {
        "view": "archive",
        "template": "articles.html",
    },
    "/:year/:month/:slug/": {
        "views": ["entry", "draft"],
        "template": "entry.html",
    },
    "/tags/:name/": {
        "filters": "intro",
        "view": "tag",
        "pagination": "/tags/:name/:num/",
        "template": "articles.html",
    },
    "/sitemap.xml": {
        "view": "sitemap",
    },
    "/feed.xml": {
        "filters": ["h2", "nohyphenate"],
        "view": "atom",
    },
    "/:slug/": {
        "view": "page",
        "template": "page.html",
    },
}


THEME = "theme"
THEME_IGNORE = ["_*", "*.xml", "main.html"]
ENGINE = "acrylamid.templates.jinja2.Environment"
DATE_FORMAT = "%d.%m.%Y, %H:%M"

STATIC_IGNORE = ["empty", "README.md"]
CONTENT_EXTENSION = ".md"

deploy_msg = "automated deployment"

commands = (
    "rm -rf output",
    "acrylamid compile",
    "git checkout gh-pages",
    "rsync -rvc --delete-after --exclude=CNAME --exclude=.git* output/ .",
    "git add .",
    "git commit -m '%s'" % deploy_msg,
    "git push origin gh-pages",
    "git checkout master",
)


DEPLOYMENT = {
    "default": " && ".join(commands),
}

import acrylamid.assets


class SASSC(acrylamid.assets.System):
    ext, target = '.scss', '.css'
    cmd = ['sassc', ]
    uses = r'^@import ["\'](?P<file>.+?\.scss)["\'];'

    def filter(self, input, directory):
        return [
            f for f in super(SASSC, self).filter(input, directory)
            if not f.split("/")[-1].startswith("_")
        ]

acrylamid.assets.SASSC = SASSC

STATIC_FILTER = ["SASSC"]

TAGLINE = "A moo-saa-fir and his undercover mission"
PRODUCT_LINK = (
    "Groovematic",
    "/",
)


TOP_NAV = (
    ("Blog", "/"),
    ("About", "/about/"),
)
BOTTOM_NAV = TOP_NAV
FEED_URL = "/feed.xml"

TWITTER = "iromli"
GPLUS = ""
SHARING = True
SHARING_TWITTER = True
SHARING_TWITTER_VIA = ""
SHARING_GPLUS = True
COPYRIGHT_YEAR = 2015
GOOGLE_FONT = "Droid+Sans:400,700"
INTRO_LINK = ""
LEGAL = "<em><a href='https://github.com/iromli/groovematic'>Use the source, Luke!</a></em>"  # noqa
# DISQUS_SHORTNAME = "groovematic"
DISQUS_SHORTNAME = ""
