# -*- coding: utf-8 -*-


class cached_property(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def spesification_state(w):
    """
    >>> assert spesification_state(u'saksı'), 'saksıyı'
    """

    v = {u'a': u'yı', u'e': u'yi', u'ı': u'yı', u'i': u'yi', u'o': u'yu',
         u'ö': u'yü', u'u': u'yu', u'ü': u'yü'}
    v2 = {u'a': u'ı', u'e': u'i', u'ı': u'ı', u'i': u'i', u'o': u'u',
          u'ö': u'ü', u'u': u'u', u'ü': u'ü'}
    lv = None
    for i in range(len(w) - 1, 0, -1):
        if w[i] in v:
            lv = w[i]
            break
    assert lv, 'Word must have at least one vowels.'
    if i == len(w) - 1:
        return w + v[lv]
    else:
        return w + v2[lv]


class GameObject(object):
    def __init__(self, *args):
        """
        All game objects must have a name, given as first argument at
        initalization.
        """
        assert len(args) > 0, 'All game objects must have at least one ' \
                              'argument that explains name of the object.'
        self.name = args[0]
        if len(args) == 2:
            self.description = args[1]

    def __repr__(self):
        return u'<GameObject: %s>' % self.name

    @cached_property
    def name_in_spesification_state(self):
        return spesification_state(self.name)


class ActiveGameObject(GameObject):

    DEFAULT_RESPONSE_WHEN_TAKEN = '<nesneyi> yerinde bıraksam daha iyi.'
    DEFAULT_RESPONSE_WHEN_DROP = '<nesneyi> bıraktım.'
    DEFAULT_RESPONSE_WHEN_READ = 'Okuyabileceğim bir şey yok.'
    DEFAULT_RESPONSE_WHEN_PUSH = 'Bu itebileceğim bir şey değil.'
    DEFAULT_RESPONSE_WHEN_PULL = 'Bu çekebileceğim bir şey değil.'

    def __init__(self, *args, **kwargs):
        self.parent_obj = kwargs.pop('parent_obj', None)

        self.can_be_taken = kwargs.pop('can_be_taken', False)
        self.response_when_taken = kwargs.pop(
            'response_when_taken', DEFAULT_RESPONSE_WHEN_TAKEN)

        self.can_be_drop = kwargs.pop(
            'can_be_drop', False)
        self.response_when_taken = kwargs.pop(
            'response_when_taken', DEFAULT_RESPONSE_WHEN_TAKEN)

        self.can_be_read = kwargs.pop(
            'can_be_read', False)
        self.response_when_read = kwargs.pop(
            'response_when_read', DEFAULT_RESPONSE_WHEN_READ)

    def get_response(key, *args, **kwargs):
        prop_name = 'response_when_%s' % key
        if not hasattr(self, prop_name):
            raise ValueError('There\'s no answer for action key: %s' % key)
        prop = getattr(self, prop_name)
        if callable(prop):
            return prop(*args, **kargs)

    def render_response(text):
        return text.replace('<nesneyi>', self.name_in_spesification_state)


class Place(GameObject):
    def __init__(self, *args, **kwargs):
        self.exits = {}
        self.objects = kwargs.pop('objects', {})
        super(Place, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Place: %s>' % self.name


class Player(GameObject):
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
