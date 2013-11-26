from acrylamid.views import View
from acrylamid.helpers import union, joinurl, event

from os.path import exists


class Archives(View):
    """Sort articles by its year.
    """
    priority = 80.0

    def init(self, conf, env, template='archives.html'):
        self.template = template

    def generate(self, conf, env, data):
        entrylist = data['entrylist']

        tt = env.engine.fromfile(self.template)
        path = joinurl(conf['output_dir'], self.path, 'index.html')

        if exists(path) and not (conf.modified or env.modified or tt.modified):
            event.skip('archive', path)
            raise StopIteration

        archives = {}
        for entry in entrylist:
            archives.setdefault(entry.year, []).append(entry)

        html = tt.render(conf=conf, articles=archives, env=union(env,
                         num_entries=len(entrylist), route=self.path))
        yield html, path
