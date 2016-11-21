
NORTH = 'N'
SOUTH = 'S'
WEST = 'W'
EAST = 'E'
PLAYING = 'P'
GAME_OVER = 'GO'

DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
GAME_STATUSES = [PLAYING, GAME_OVER]


class GameObject(object):
    def __init__(self, *args, **kwargs):
        """
        All game objects must have a name, given as first argument at
        initalization.

        >>> _object = GameObject('Foo')
        >>> _object = GameObject()
        Traceback (most recent call last):
         ...
        AssertionError: All game objects must have at least one argument that
        explains name of the object
        """
        assert len(args) > 0, 'All game objects must have at least one ' \
                              'argument that explains name of the object'
        self.name = args[0]

    def __repr__(self):
        return '<GameObject: %s>' % self.name


class Container(list):
    """
    Containers are list like objects that can only hold one object with
    same name. Also you can get an object from list with calling it's name.

    >>> class Foo(GameObject):
    >>>     pass
    >>> class FooContainer(Container):
    >>>    obj_type = Foo
    >>> container.append(GameObject('Telephone'))
    >>> container.get('Telephone')
    <GameObject: Telephone>
    """
    name_map = {}
    obj_type = None

    SUBCLASS_ERR_TEXT = 'This container only hold objects that inherited ' \
                        'from %s.'

    DUPLICATE_ERR_TEXT = 'Object with this name is already exists.'

    def append(self, value):
        assert issubclass(value.__class__, self.obj_type), \
               self.SUBCLASS_ERR_TEXT % self.obj_typE
        assert value.name not in self.name_map, \
               self.SUBCLASS_ERR_TEXT
        self.name_map[value.name] = value
        super(Container, self).append(value)
 
    def get(self, name):
        return self.name_map[name]


class Place(GameObject):

    """
    Places in game. They contain objects and exits.
    """

    def __init__(self, *args, **kwargs):
        super(Place, self).__init__(*args)
        self.description = kwargs.pop('description', None)
        self.exits = {}
        self.objects = ObjectContainer()

        for _object in kwargs.pop('objects', []):
            self.objects.append(_object)
 

class PlaceContainer(Container):

    obj_type = Place

    def connect(self, place1_name, direction, place2_name):
        self.get(place1_name).exits[direction] = self.get(place2_name)

    def add_object(self, place_name, game_object):
        place = self.get(place_name)
        place.objects.append(game_object)
        game_object.place = place


class ObjectContainer(Container):
    obj_type = GameObject


class Game(object):

    def __init__(self, name, author=None, version='0.0'):
        self.name = name
        self.author = author
        self.version = version
        self.status = PLAYING
        self.places = PlaceContainer()

    def start(self, player):
        print player.place.title
        print player.place.description


class Human(GameObject):
    def __init__(self, *args, **kwargs):
        super(Human, self).__init__(*args, **kwargs)
        self.hitpoints = kwargs.pop('hitpoints')


class Player(Human):
    pass
if __name__ == '__main__':
    import doctest
    doctest.testmod()
