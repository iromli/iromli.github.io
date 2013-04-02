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
    '/': {'view': 'archives'},
    '/:year/:month/:slug/': {'views': ['entry', 'draft']},
    '/tag/:name/': {
        'view': 'tag',
        'pagination': '/tag/:name/:num/'
    },
    '/atom.xml': {'filters': ['nohyphenate'], 'view': 'atom'},
    '/rss.xml': {'filters': ['nohyphenate'], 'view': 'rss'},
    # '/sitemap.xml': {'view': 'sitemap'},
    '/:slug/': {'view': 'page', 'template': 'flatpage.html'},

}

THEME = 'theme'
ENGINE = 'acrylamid.templates.jinja2.Environment'
DATE_FORMAT = '%d.%m.%Y, %H:%M'

VIEWS_DIR = 'views'
STATIC = ['assets']
STATIC_IGNORE = ['empty', 'README.md']

DISQUS_SHORTNAME = 'groovematic'

CONTENT_IGNORE = ['drafts/*']
