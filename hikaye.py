# -*- coding: utf-8 -*-

NORTH = 'N'
SOUTH = 'S'
WEST = 'W'
EAST = 'E'

PLAYING = 'P'
GAME_OVER = 'GO'

DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
GAME_STATUSES = [PLAYING, GAME_OVER]


def reverse_direction(direction):
    return {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}[direction]


class cached_property(object):
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class Word(object):
    """
    """

    llv_accusative_case_suffixes = {
        u'a': u'yı', u'e': u'yi', u'ı': u'yı', u'i': u'yi', u'o': u'yu',
        u'ö': u'yü', u'u': u'yu', u'ü': u'yü'
    }

    llo_accusative_case_suffixes = {
        u'a': u'i', u'e': u'i', u'ı': u'ı', u'i': u'i', u'o': u'u',
        u'ö': u'ü', u'u': u'u', u'ü': u'ü'
    }

    llv_genetive_case_suffixes = {
        u'a': u'nın', u'e': u'nin', u'ı': u'nın', u'i': u'nin', u'o': u'nun',
        u'ö': u'nün', u'u': u'nun', u'ü': u'nün'
    }

    llo_genetive_case_suffixes = {
        u'a': u'in', u'e': u'in', u'ı': u'ın', u'i': u'in', u'o': u'un',
        u'ö': u'ün', u'u': u'un', u'ü': u'ün'
    }

    def __init__(self, word):
        self.word = word

    def get_last_vowel_info(self):
        """
        >>> assert Word('saat').get_last_vowel_info() == (False, 'a')
        >>> assert Word('puma').get_last_vowel_info() == (True, 'a')
        """
        w = self.word
        v = self.llv_accusative_case_suffixes
        lv = None
        for i in range(len(w) - 1, -1, -1):
            if w[i] in v:
                lv = w[i]
                break
        if not lv:
            return False, False
        if i == len(w) - 1:
            return True, lv
        return False, lv

    def accusative(self):
        """
        >>> assert Word('saat').accusative() == 'saati'
        """
        is_vowel_last_letter, vowel = self.get_last_vowel_info()
        if is_vowel_last_letter:
            return self.word + self.llv_accusative_case_suffixes[vowel]
        else:
            return self.word + self.llo_accusative_case_suffixes[vowel]

    def is_accusative(self):
        """
        >>> assert Word('saati').is_accusative() == (True, 'i')
        """
        is_vowel_last_letter, vowel = self.get_last_vowel_info()
        if not is_vowel_last_letter:
            suffixes = self.llv_accusative_case_suffixes.values()
        else:
            suffixes = self.llo_accusative_case_suffixes.values()
        found = filter(self.word.endswith, suffixes)
        if found:
            return True, found[0]
        return False, ''

    def genetive(self):
        """
        >>> assert Word('saat').genetive() == 'saatin'
        """
        is_vowel_last_letter, vowel = self.get_last_vowel_info()
        if is_vowel_last_letter:
            return self.word + self.llv_genetive_case_suffixes[vowel]
        else:
            return self.word + self.llo_genetive_case_suffixes[vowel]

    def is_genetive(self):
        """
        >>> assert Word('saatin').is_genetive() == (True, 'in')
        """
        is_vowel_last_letter, vowel = self.get_last_vowel_info()
        if is_vowel_last_letter:
            suffixes = self.llv_genetive_case_suffixes.values()
        else:
            suffixes = self.llo_genetive_case_suffixes.values()
        found = filter(self.word.endswith, suffixes)
        if found:
            return True, found[0]
        return False, ''


class GameObjectView(object):
    @staticmethod
    def display(_object):
        print _object.name
        if _object.description:
            print '-' * len(_object.name)
            print _object.description

    @staticmethod
    def out(text):
        print text


class BaseGameObject(object):
    def __init__(self, name, description=None, parent=None):
        self.name = name.lower()
        self.description = description
        self.children = []
        self.parent = None
        self.view = GameObjectView
        if parent:
            self.set_parent(parent)

    def __repr__(self):
        return u'<GameObject: %s>' % self.name

    def set_parent(self, something):
        self.parent = something
        something.children.append(self)


class Place(BaseGameObject):
    def __init__(self, *args, **kwargs):
        super(Place, self).__init__(*args, **kwargs)
        self.exits = {}

    def connect(self, other_place, direction):
        self.exits[direction] = other_place
        other_place.exits[reverse_direction(direction)] = self


class GameObject(BaseGameObject):
    pass


class PlayerController(object):

    DEFAULT_ACTION_RESPONSES = {
        'take': u'Bunu yerinde bıraksam daha iyi olacak.',
        'read': u'Üzerinde okuyacak bir şey göremedim.',
        'taste': u'Bu şeyi ağzıma sokmasam daha iyi olacak.',
        'eat': u'Bunu yapabileceğimi hiç ama hiç sanmıyorum.',
        'pull': u'Bu olduğu yere sabitlenmiş.',
        'push': u'Gücüm buna asla yetmez.'
    }

    commands = {

        u'<nesneyi> oku': 'read',
        u'<nesneyi> tat': 'taste',
        u'<nesneyi> ye': 'eat',
        u'<nesneyi> al': 'take',
        u'<nesneyi> aç': 'open',
        u'<nesneyi> incele': 'examine',

        u'<nesneyi> <nesnenin> içine koy': 'put_smth_into_smth',
        u'<nesneye> <nesne> ile vur': 'hit_smth_with_smth',

        u'kuzeye git': 'go_north',
        u'güneye git': 'go_south',
        u'doğuya git': 'go east',
        u'batıya git': 'go west',
    }

    def __init__(self, player):
        self.player = player

    def get_default_action_response(self, action_name):
        return self.DEFAULT_ACTION_RESPONSES.get(
            action_name, 'Bunu yapamıyorum.')

    def action_method_name(self, action_name):
        return 'response_when_%s' % action_name

    def do_action_on(self, something, action_name, *args, **kwargs):
        action_method_name = self.action_method_name(action_name)
        if hasattr(self, action_method_name):
            return getattr(something, action_method_name)(*args, **kwargs)
        return self.get_default_action_response(action_name)

    def read(self, something):
        return self.do_action_on(something, 'read')

    def taste(self, something):
        return self.do_action_on(something, 'taste')

    def take(self, something):
        return self.do_action_on(something, 'take')

    def eat(self, something):
        return self.do_action_on(something, 'eat')


class InventoryView(GameObjectView):
    @staticmethod
    def display(_object):
        print 'Çantamda şunlar var:'
        for child in _object.children:
            print child.view.display(child)
            print "----"


class Bag(GameObject):
    def __init__(self, *args, **kwargs):
        super(Bag, self).__init__(*args, **kwargs)
        self.view = InventoryView


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__('Oyuncu')
        self.controller = PlayerController(self)
        self.inventory = Bag('Çantam', parent=self)

    def interractable_objects(self):
        return self.inventory.children + self.place.children


class Game(GameObject):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.player = Player()
        self.status = PLAYING
        self.player.set_parent(kwargs.pop('start_point'))
        super(Game, self).__init__(*args, **kwargs)


class Interpreter(object):

    converters = {
        'accusative': '<nesneyi>',
        'genetive': '<nesnenin>',
    }

    def __init__(self, game=None):
        self.game = game

    def parse_input(self, text):
        names = []
        for name_case, converted_string in self.converters.items():
            checker_method = 'is_' + name_case
            for word in text.split():
                hit, suffix = getattr(Word(word), checker_method)()
                if hit:
                    text = text.replace(word, converted_string)
                    names.append((word, name_case))
        return text, names

    def find_controller_method(self, input_command):
        command_controllers = [self.game.player.controller, ]
        found_command = None
        for command_controller in command_controllers:
            for command, method in command_controller.commands.iteritems():
                if command == input_command:
                    return command_controller, method
        return None, None

    def find_objects(self, names):
        objects = self.game.player.inventory.children +\
            self.game.player.parent.children
        found_objects = []
        for name, name_case in names:
            for obj in objects:
                obj_case_name = getattr(Word(obj.name), name_case)()
                if obj_case_name == name:
                    found_objects.append(obj)
        return found_objects

    def get_input(self, text=u'Ne yapmak istiyorsun?'):
        response = raw_input('\n' + text + '\n>').decode('utf-8').lower()
        import ipdb; ipdb.set_trace()
        command, names = self.parse_input(response)
        controller, method = self.find_controller_method(command)
        if not controller:
            print u'Anlayamadım'
            return
        objects = self.find_objects(names)
        if not objects:
            print u'Etrafta %s göremedim.' % names[0][0]
            return
        print getattr(controller, method)(*objects)

    def run(self):
        self.game.player.parent.view.display(self.game.player.parent)
        while self.game.status == PLAYING:
            self.get_input()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
