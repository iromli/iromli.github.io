from acrylamid.views.articles import Articles


class Homepage(Articles):
    def init(self, template='home.html'):
        super(Homepage, self).init(template)
