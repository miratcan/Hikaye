# -*- coding: utf-8 -*-

from hikaye import Game, Place, GameObject
from hikaye import NORTH, SOUTH, WEST, EAST
from hikaye import Interpreter


class Leaflet(GameObject):
    def response_when_read(self):
        return u"Apartmanın içinde acayip sesler var. Günlerdir dışarıya "\
               u"çıkmadım. Yiyeceğim bitiyor. Kapıyı açıp yangın merdivenine "\
               u"kadar ulaşabilirsem kaçıp yardım isteyebilirim."

garden = Place(u'Bahçe')
kitchen = Place(u'Mutfak',
                u'Karşımdaki tezgahın üzeri bomboş. Anlaşılan burayı terk '
                u'etmeden önce her şeyi düzenli bir şekilde bırakmak '
                u'istemişler. Tezgahın bittiği yerde bir masa ve 2 tane '
                u'sandalye var. Masanın üzerinde bir kağıt parçası duruyor. ')

kitchen.connect(garden, NORTH)

leaflet = Leaflet(u'Gemi', parent=kitchen)

game = Game('uTest Oyunu', author='Mirat', start_point=kitchen)

interpreter = Interpreter(game)
interpreter.run()
