# -*- encoding: utf-8 -*-
# This is your configuration file.  Please write valid python!
# See http://posativ.org/acrylamid/conf.py.html

SITENAME = 'Groovematic'
WWW_ROOT = 'http://groovematic.com/'

AUTHOR = 'Isman Firmansyah'
EMAIL = 'isman.firmansyah@gmail.com'

FILTERS = [
    'markdown+extra+codehilite',
]

VIEWS = {
    "/": {"view": "archive", "template": "archives.html"},
    '/:year/:month/:slug/': {'views': ['entry', 'draft']},
    '/tags/:name/': {
        'view': 'tag',
        'pagination': '/tags/:name/:num/',
        "template": "tags.html",
    },
    '/atom.xml': {'filters': ['nohyphenate'], 'view': 'atom'},
    # '/rss.xml': {'filters': ['nohyphenate'], 'view': 'rss'},
    # '/sitemap.xml': {'view': 'sitemap'},
    '/:slug/': {'view': 'page', 'template': 'flatpage.html'},

}

THEME = 'theme'
ENGINE = 'acrylamid.templates.jinja2.Environment'
DATE_FORMAT = '%d.%m.%Y, %H:%M'

STATIC_IGNORE = ['empty', 'README.md']
CONTENT_EXTENSION = [".md"]

DISQUS_SHORTNAME = 'groovematic'

deploy_msg = "automated deployment"

commands = (
    "rm -rf output",
    "acrylamid compile",
    "git checkout gh-pages",
    "rsync -rvc --delete-after --exclude=CNAME --exclude=.git* output/ .",
    "git add .",
    "git commit -am '%s'" % deploy_msg,
    "git push origin gh-pages",
    "git checkout master",
)


DEPLOYMENT = {
    "default": " && ".join(commands),
}
