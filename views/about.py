from acrylamid.views.articles import Articles


class About(Articles):
    def init(self, template='about.html'):
        super(About, self).init(template)
