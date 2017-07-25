# -*- coding: utf-8 -*-

from hikaye import Game
from hikaye import GameObject
from hikaye import PlaceContainer, ObjectContainer
from hikaye import Place
from hikaye import NORTH, SOUTH, WEST, EAST

"""
          ------------
          |  Koridor |
          |  Kuzey   |
          |          |
|---------|          |---------|
| Çalışma |  Koridor |         |
| Odası   |   Güney  | Mutfak  |
|---------|----------|---------|
          |   Antre  |
          |----------|
          | Kapı Önü |
          |----------|
"""

game = Game(
    "İstanbul Efsaneleri",
    "2001 Yılının sonbaharı, İstanbul'un eski semtlerinden birinde ailesiyle "
    "yaşayan 16 yaşında bir çocuksun. Futbol maçı yapmak mahalledeki "
    "arkadaşlarınla birlikte her zaman gittiğiniz boş araziye gitmişsiniz "
    "Terletmeyen bir hava var, yaprakların sesi koşma, nefes "
    "nefese kalma ve bağırışma seslerinize karışıyor. "
    "Top oyunculardan birinin sert vuruşuyla hemen yan bahçedeki terk "
    "edilmiş evin penceresinden içeri camı kırarak giriyor. Topu kimin "
    "alacağını tartışan arkadaşlarının lafını 'ben alırım' diyerek "
    "kesiyorsun. Arazi ile terk edilmiş evin bahçesi3 alçak bir "
    "duvar ile ayrılıyor. Duvarı atlayıp evin kapısının önüne gidiyorsun.",
    author='Mirat Can Bayrak',)


""" ------------------------------- Objects ------------------------------- """

game.objects = ObjectContainer([
    GameObject(
        u'Saksı',
        u'Uzun kahverengi bir saksı. Üzerindeki bitki kurumuş. '
        u'saksının içindeki toprak kaskatı ve yıllardır sulanmamış.'),
    GameObject(
        u'Kapı',
        u'Demirden yapılmış, dokunmaya tiksinecek kadar tozlu ve yağlı.'
    ),
    GameObject(
        u'Ayakkabilar',
        u'Demirden yapılmış, dokunmaya tiksinecek kadar tozlu ve yağlı.'
    )]
)

""" -------------------------------- Places ------------------------------- """

game.places = PlaceContainer([
    Place(
        u"Kapının Önü",
        u"Tam önünde demir kapı, sağ tarafında ise bir saksı var. Bunun "
        u"dışında borulara asılı bir ayakkabı çekeceği görüyorsun.",
    ),
    Place(
        u"Antre",
        u"Biraz onceki aydinlik hal yok oldu. Burasi oldukca serin. "
        u"Yerde bir çift ayakkabı var. Kuzeyde uzunca bir koridorun güney ucu",
        objects=[game.objects.get(u'Ayakkabilar')]
    ),
    Place(
        "Koridor Güney",
        "Batı ve doğu tarafta iki oda var. Kuzeyde ise koridorun kuzey ucu."
    ),
    Place(
        "Çalışma Odası",
        "Odada büyük kahverengi bir kitaplık, üzerinde bir sürü eşya olan "
        "bir çalışma masası mevcut. Duvarda sarı kağıtlara pastel ile "
        "çizilmiş resimler görüyorsun. Odanın tamamı yetişkin birine aitmiş "
        "gibi gözükse de duvardaki resimler bir çocuğa ait gibi gözüküyor."
    ),
    Place(
        "Mutfak",
        "Burası oldukça küçük bir mutfak. Doğu tarafta paslı metal lavabonun "
        "üstündeki ahşap pencereden maç yaptığınız araziyi görebiliyorsun."
        "Tavandan bir takım takırtılar geliyor."
    ),
    Place(
        "Salon",
        "Radyo mumlar tek bir koltuk.")
])

""" ----------------------- Place Connections ----------------------------- """

game.player.place = game.places.get('Kapının Önü')

""" ------------------------- Game Setup ---------------------------------- """

game.places.connect('Kapının Önü', NORTH, 'Antre')
game.places.connect('Antre', NORTH, 'Koridor Güney')

game.places.connect('Koridor Güney', WEST, 'Çalışma Odası')
game.places.connect('Koridor Güney', EAST, 'Mutfak')

""" ------------------------- Game Setup ---------------------------------- """
game.controller.start()
