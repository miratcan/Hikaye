from re import sub
from sys import stdout
from random import choice, randint
from time import sleep
from textwrap import wrap

NORTH = 'N'
SOUTH = 'S'
WEST = 'W'
EAST = 'E'

PLAYING = 'P'
GAME_OVER = 'GO'

DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
GAME_STATUSES = [PLAYING, GAME_OVER]

MAX_WIDTH = 79

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


class Controller(object):
    """
    COMMANDS are lists that contains information in this template:
    ((command_name, alternative_name1, alternative_name2), method_to_run,
     description))
    """

    def examine(self):
        self.obj.view.display()

    def register(self, func, aliases):
        if not hasattr(func.im_func, '__aliases__'):
            func.im_func.__aliases__ = []
        for alias in aliases:
            if not alias in func.im_func.__aliases__:
                func.im_func.__aliases__.append(alias)
        if not hasattr(self, 'commands'):
            self.commands = type("", (), {})()
        setattr(self.commands, func.__name__, func)

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.register(self.examine, ('examine', 'x'))
        super(Controller, self).__init__()

class PlayerController(Controller):

    def go_somewhere(self, way):
        """
        >>> place1 = Place('Place1')
        >>> place2 = Place('Place2')
        >>> place3 = Place('Place3')
        >>> places = PlaceContainer((place1, place2, place3))
        >>> places.connect('Place1', NORTH, 'Place2')
        >>> places.connect('Place2', NORTH, 'Place3')
        >>> player = Player('Tomb Raider')
        >>> player.place = place1
        >>> player.place
        <Place: Place1>
        >>> player.controller.cmd_go_north()
        Place2
        ------
        >>> player.place
        <Place: Place2>
        >>> player.controller.cmd_go_north()
        Place3
        ------
        >>> player.place
        <Place: Place3>
        """
        assert hasattr(self.obj, 'place'), 'Player is at nowhere.'
        assert way in self.obj.place.exits, 'Can not go that way!'
        self.obj.place = self.obj.place.exits[way]
        self.obj.place.view.display()

    def go_north(self):
        return self.go_somewhere(NORTH)

    def go_south(self):
        return self.go_somewhere(SOUTH)

    def go_west(self):
        return self.go_somewhere(WEST)

    def go_east(self):
        return self.go_somewhere(EAST)

    def __init__(self, obj):
        super(PlayerController, self).__init__(obj)
        self.register(self.go_north, ('go north', 'n'))
        self.register(self.go_south, ('go south', 's'))
        self.register(self.go_west, ('go west', 'w'))
        self.register(self.go_east, ('go east', 'e'))


class ViewBase(object):
    def __init__(self, obj):
        self.obj = obj


class PrintView(ViewBase):

    def clean(self, line):
        result = line
        result = sub(' +', ' ', line)
        result = line.replace('<', '')
        return result

    def _print(self, line):
        print self.clean(line)

    def display(self):
        self._print(self.obj.name)
        self._print('-' * len(self.obj.name))
        if hasattr(self.obj, 'description'):
            self._print(self.obj.description + '\n')


class TypeWriterView(ViewBase):

    TYPING_SPEED = (1.0 / 200,)
    # TYPING_SPEED = (0.05,)

    def clean(self, line):
        result = line
        result = sub(' +', ' ', line)
        return result

    def _print(self, line):
        line = self.clean(line)
        for char in line:
            if char == '<':
                char = '\b \b'
                sleep(0.2)
            stdout.write(char)
            stdout.flush()
            speed = choice(self.TYPING_SPEED)
            sleep(speed)
        stdout.write('\n')
        stdout.flush()

    def display(self):
        self._print(self.obj.name)
        name_length = len(self.obj.name)
        self._print(('-' * (name_length - 4)))
        if hasattr(self.obj, 'description'):
            self._print(self.obj.description + '\n')

View = PrintView


class HasController(object):

    def __init__(self, *args, **kwargs):
        super(HasController, self).__init__(*args, **kwargs)
        self.controller = self.init_controller()

    def init_controller(self):
        return self.CONTROLLER_CLASS(self)


class HasView(object):
    def __init__(self, *args, **kwargs):
        """
        >>> class C1(HasView): VIEW_CLASS=View
        >>> c1 = C1()
        >>> assert hasattr(c1, 'view') == True
        """
        super(HasView, self).__init__(*args, **kwargs)
        self.view = self.init_view()

    def init_view(self):
        return self.VIEW_CLASS(self)


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
    AssertionError: This container only hold objects that inherited from \
<class '__main__.Foo'>.

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


class Place(HasView, GameObject):

    """
    Places in game. They contain objects and exits.
    """
    VIEW_CLASS = View

    def __init__(self, *args, **kwargs):
        """
        A place can be initialized with a description:

        >>> place = Place('House of King', 'Very nice decorated place')
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
        self.exits = {}
        self.objects = ObjectContainer()

        for _object in kwargs.pop('objects', []):
            self.objects.append(_object)
        super(Place, self).__init__(*args, **kwargs)

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


class Player(HasController, HasView, Human):

    VIEW_CLASS = View
    CONTROLLER_CLASS = PlayerController

    def __repr__(self):
        return '<Player: %s>' % self.name


class GameView(View):
    def display(self):
        title_1 = self.obj.name
        self._print('\n\n' + title_1 + '\n\n')
        if hasattr(self.obj, 'description'):
            self._print(self.obj.description + '\n')


class GameController(Controller):
    def start(self):
        self.obj.view.display()
        self.obj.player.place.view.display()
        while self.obj.status is not GAME_OVER:
            self.obj.input.run(self.obj.input.get_input())


class InputParser(object):
    """
    This object parses input, finds command about given input and runs
    method on conroller with given input.
    """

    def __init__(self, game):
        self.game = game
        self.message = 'What do you want to do?'

    def get_available_commands(self):
        """
        Finds commands from current game, place, player, player inventory and
        places.
        >>> game = Game('Title', 'Description')
        >>> game.places.append(Place('Title', 'Description'))
        >>> game.player.place = game.places.get('Title')
        >>> for obj, commands in game.input.get_available_commands().iteritems():
        ...     print obj
        ...     for command in commands:
        ...         print command
        Title game by None
        <examine command that runs: cmd_examine method>
        <open command that runs: cmd_open method>
        <Player: Player>
        <go north command that runs: cmd_go_north method>
        <go south command that runs: cmd_go_south method>
        <go west command that runs: cmd_go_west method>
        <go east command that runs: cmd_go_east method>
        """
        _commands = {
            self.game: self.game.controller.commands,
            self.game.player: self.game.player.controller.commands,
        }
        return _commands

    def get_input(self):
        result = raw_input(self.message)
        print
        return result

    def find_command(self, text):
        for obj, commands in self.get_available_commands().iteritems():
            for command in dir(commands):
                method = getattr(commands, command)
                if hasattr(method, '__aliases__') and text in \
                   method.__aliases__:
                    return obj, method

    def run(self, text):
        command = self.find_command(text)
        if not command:
            self.game.view._print('What?\n')
            return
        obj, command = command
        command()


class Game(HasView, HasController):

    CONTROLLER_CLASS = GameController
    VIEW_CLASS = GameView

    def __init__(self, name, description, author=None, version='0.0'):
        """
        Container for game state.

        >>> game = Game('Nameless Guest', None, author='Mirat')
        >>> print game
        Nameless Guest game by Mirat

        Add places.

        >>> game.places.append(Place('My Room', "It is so dark here."))
        >>> game.places.append(Place('Corridor', 'A radio playing'))
        >>> game.places.append(Place('Bathroom', 'I see my face!'))

        Connect the places:

        >>> game.places.connect('My Room', NORTH, 'Corridor')
        >>> game.places.connect('Corridor', NORTH, 'Bathroom')
        >>> game.places.get('My Room').exits
        {'N': <Place: Corridor>}
        >>> game.places.get('Bathroom').exits
        {'S': <Place: Corridor>}
        """
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.status = PLAYING
        self.places = PlaceContainer()
        self.player = Player('Player')
        self.input = InputParser(self)
        super(Game, self).__init__()

    def __repr__(self):
        """Representation for game object."""
        return '%s game by %s' % (self.name, self.author)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
