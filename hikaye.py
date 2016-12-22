from random import choice, randint
import sys
from time import sleep

NORTH = 'N'
SOUTH = 'S'
WEST = 'W'
EAST = 'E'

PLAYING = 'P'
GAME_OVER = 'GO'

DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
GAME_STATUSES = [PLAYING, GAME_OVER]

TYPING_SPEED = (0.05, 0.07, 0.1, 0.15)

"""
Before commiting any changes check this file with:
python hikaye.py
pep8 hikaye.py
pep257 hikaye.py
"""


def reverse_direction(direction):
    """Reverse given direction.

    >>> reverse_direction(NORTH) == SOUTH
    True
    >>> reverse_direction(SOUTH) == NORTH
    True
    >>> reverse_direction(WEST) == EAST
    True
    >>> reverse_direction(EAST) == WEST
    True
    """
    return {NORTH: SOUTH, SOUTH: NORTH,
            WEST: EAST, EAST: WEST}[direction]


def _print(line, constant_speed=False):
    for char in line:
        if char == '<':
            char = '\b \b'
            sleep(0.2)
        sys.stdout.write(char)
        sys.stdout.flush()
        if constant_speed:
            speed = 0.1
        else:
            speed = choice(TYPING_SPEED)
        sleep(speed)
    sys.stdout.write('\n')
    sys.stdout.flush()

class GameObject(object):

    """Base for all game objects."""

    def __init__(self, *args, **kwargs):
        """
        All game objects must have a name, given as first argument at
        initalization.

        >>> _object = GameObject('Foo')
        >>> _object = GameObject()
        Traceback (most recent call last):
         ...
        AssertionError: All game objects must have at least one argument \
that explains name of the object.
        """
        assert len(args) > 0, 'All game objects must have at least one ' \
                              'argument that explains name of the object.'
        self.name = args[0]

        if len(args) == 2:
           self.description = args[1]

    def __repr__(self):
        """Representation for GameObject."""
        return '<GameObject: %s>' % self.name


class Container(list):

    """
    Containers are list like objects that can only hold one object with
    same name. Also you can get an object from list with calling it's name.

    >>> class Foo(GameObject): pass
    >>> class FooContainer(Container): obj_type=Foo
    >>> container = FooContainer()

    The container that we specified can contain Foo objects.

    >>> container.append(Foo('Mirat'))

    If we try to add another kind of object it will raise error.

    >>> container.append(None)
    Traceback (most recent call last):
    ...
    AssertionError: This container only hold objects that inherited
    from <class '__main__.Foo'>.

    Also containers are list but they can call objects with their names.

    >>> container.get('Mirat')
    <GameObject: Mirat>

    Also containers can be initialized like lists.

    >>> container = FooContainer((Foo('Mirat'), Foo('Ayfer')))
    >>> container.get('Ayfer')
    <GameObject: Ayfer>
    >>> container.get('Mirat')
    <GameObject: Mirat>
    """

    name_map = {}
    obj_type = None

    SUBCLASS_ERR_TEXT = 'This container only hold objects that inherited ' \
                        'from %s.'

    DUPLICATE_ERR_TEXT = 'Object with this name is already exists.'

    def __init__(self, *args):
        if args:
            for item in args[0]:
                self.name_map[item.name] = item
        super(Container, self).__init__(*args)

    def append(self, value):
        assert issubclass(value.__class__, self.obj_type), \
            self.SUBCLASS_ERR_TEXT % self.obj_type
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
        """
        A place can be initialized with a description:

        >>> place = Place('House of King',
        >>>     description='Very nice decorated place')
        >>> place
        <Place: House of King>
        >>> place.description
        'Very nice decorated place'

        Also a place can contain objects:

        >>> rope = GameObject('Rope')
        >>> place = Place('Hunter Hut', objects=[rope])
        >>> print place
        <Place: Hunter Hut>
        >>> print place.objects
        [<GameObject: Rope>]
        """
        super(Place, self).__init__(*args)
        self.exits = {}
        self.objects = ObjectContainer()

        for _object in kwargs.pop('objects', []):
            self.objects.append(_object)

    def __repr__(self):
        return '<Place: %s>' % self.name


class PlaceContainer(Container):
    """
    Container for places. They have ability to connect places together and
    """

    obj_type = Place

    def connect(self, place1_name, direction, place2_name):
        """Connect two places together. This method used to build maps.

        >>> king_house = Place('House of King')
        >>> a_forest = Place('Forest')
        >>> places = PlaceContainer((king_house, a_forest))
        >>> print places
        [<Place: House of King>, <Place: Forest>]
        >>> places.connect('House of King', NORTH, 'Forest')
        >>> king_house.exits
        {'N': <Place: Forest>}
        >>> a_forest.exits
        {'S': <Place: House of King>}
        """
        self.get(place1_name).exits[direction] = self.get(place2_name)
        self.get(place2_name).exits[reverse_direction(direction)] \
            = self.get(place1_name)

    def add_object(self, place_name, game_object):
        """ Adds object to place.

        >>> lamer_house = Place('Lamer House')
        >>> television = GameObject('Television')
        >>> places = PlaceContainer((lamer_house,))
        >>> places.add_object('Lamer House', television)
        >>> places.get('Lamer House').objects
        [<GameObject: Television>]
        >>> places.get('Lamer House').objects
        [<GameObject: Television>]
        """
        place = self.get(place_name)
        place.objects.append(game_object)
        game_object.place = place


class ObjectContainer(Container):
    obj_type = GameObject


class Creature(GameObject):
    """
    Base model for all living creatures in game.
    """
    HITPOINTS = 30
    DEXERITY = 30
    STRENGTH = 30

    def __init__(self, *args, **kwargs):
        super(Creature, self).__init__(*args, **kwargs)
        self.hitpoints = kwargs.pop('hitpoints', self.HITPOINTS)


class Human(Creature):
    HITPOINTS = 100
    DEXERITY = 60
    STRENGTH = 30


class Player(Human):
    def look_around(self):
        _print(self.place.name)
        name_length = len(self.place.name)
        wrong_length = randint(3, 8)
        _print(('-' * (name_length + wrong_length)) + \
                '<' * wrong_length, constant_speed=True)
        if self.place.description:
            _print(self.place.description)


class Game(object):

    def __init__(self, name, author=None, places=[], version='0.0'):
        """
        Container for game state.

        >>> place_1 = Place('My Room',
        >>>     description="It is so dark here, I can not see anything")
        >>> place_2 = Place('Corridor',
        >>>     description='A radio playing')
        >>> place_3 = Place('Bathroom', description='I see my face!')
        >>> game = Game('Nameless Guest', author='Mirat',
        >>>     places=[place_1, place_2, place_3])
        >>>
        >>> print game
        Nameless Guest game by Mirat

        Let's connect the rooms:

        >>> game.places.connect('My Room', NORTH, 'Corridor')
        >>> game.places.connect('Corridor', NORTH, 'Bathroom')
        >>> game.places.get('My Room').exits
        {'N': <Place: Corridor>}
        >>> game.places.get('Bathroom').exits
        {'S': <Place: Corridor>}
        """
        self.name = name
        self.author = author
        self.version = version
        self.status = PLAYING
        self.places = PlaceContainer(places)
        self.player = Player('Player')

    def start(self):
        _print('\n' * 20)
        self.player.look_around()

    def __repr__(self):
        """Representation for game object."""
        return '%s game by %s' % (self.name, self.author)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
