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

kitchen = Place(
    u'Mutfak',
    u'Karşımdaki tezgahın üzeri bomboş. Anlaşılan burayı terk etmeden önce '
    u'her şeyi düzenli bir şekilde bırakmak istemişler. Tezgahın bittiği '
    u'yerde bir masa ve 2 tane sandalye var. Masanın üzerinde bir *kağıt* '
    u'duruyor. Tezgahın üzerinde boş plastik bir su şişesi var.')

kitchen.connect(garden, NORTH)

leaflet = Leaflet(u'Gemi', parent=kitchen)

game = Game(
    u'Test Oyunu',
    u'Evimin önüne geldiğimde tam anahtarlarımı çıkarıyordum ki karşı '
    u'dairenin kapısının aralık olduğunu gördüm.',
    author='Mirat Can Bayrak',
    start_point=kitchen)

game.controller.start()