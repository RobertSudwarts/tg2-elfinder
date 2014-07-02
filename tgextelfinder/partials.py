from tg import expose

@expose('tgextelfinder.templates.little_partial')
def something(name):
    return dict(name=name)