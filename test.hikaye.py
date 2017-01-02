# -*- coding: utf-8 -*-

from hikaye import Game
from hikaye import GameObject
from hikaye import PlaceContainer, ObjectContainer
from hikaye import Place
from hikaye import NORTH

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
    "kesiyorsun. Arazi ile terk edilmiş evin bahçesi alçak bir "
    "duvar ile ayrılıyor. Duvarı atlayıp evin kapısının önüne gidiyorsun.",
    author='Mirat Can Bayrak',)

""" ------------------------------- Objects ------------------------------- """

game.objects = ObjectContainer([
    GameObject(
        'Saksı',
        'Uzun kahverengi bir saksı. Üzerindeki bitki kurumuş. '
        'saksının içindeki toprak kaskatı ve yıllardır sulanmamış. '),
    GameObject(
        'Kapı',
        'Demirden yapılmış, dokunmaya tiksinecek kadar tozlu ve yağlı.'
    )]
)

""" -------------------------------- Places ------------------------------- """

game.places = PlaceContainer([
    Place(
        "Kapının Önü",
        "Tam önünde demir kapı, sağ tarafında ise bir saksı var. Bunun "
        "dışında borulara asılı bir ayakkabı çekeceği görüyorsun.",
    ),
    Place(
        "Antre",
        "Biraz onceki aydinlik hal yok oldu. Burasi oldukca serin. "
        "Sag tarafta calisma odasinin girisi mecvut. Sol tarafta ise misafir "
        "yatak odasinin girisi."
    )
])

""" ------------------------- Place Connections --------------------------- """

game.player.place = game.places.get('Kapının Önü')

""" ------------------------- Game Setup ---------------------------------- """

game.places.connect('Kapının Önü', NORTH, 'Antre')

""" ------------------------- Game Setup ---------------------------------- """

game.controller.start()
game.player.controller.cmd_go_north()
