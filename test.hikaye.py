from hikaye import Game
from hikaye import PlaceContainer
from hikaye import Place
from hikaye import NORTH

places = PlaceContainer([
    Place(
        'Evin Yatak Odasi',
        'Burasi pek de modern olmayan esyalarla dosenmis. Karsinda bir elbise dolabi ' \
        'sol tarafinda ise pencere var. Sag tarafta cekmeceli baska bir dolap ve onun ' \
	'uzerinde duz bir ayna mevcut. Odanin ici aydinlik. Pencereden gelen sari sicak ' \
	'isik gunun erken saatlerinde oldugunu anlamana yetiyor.'
    ),
    Place(
        'Koridor',
	'Biraz onceki aydinlik hal yok oldu. Burasi oldukca serin. '
	'Sag tarafta calisma odasinin girisi mecvut. Sol tarafta ise misafir yatak odasinin ' \
        'girisi.'
    )
])

places.connect('Evin Yatak Odasi', NORTH, 'Koridor')

game = Game('Depremden Kurtul', author='Mirat Can Bayrak', places=places)

game.player.place = game.places.get('Evin Yatak Odasi')

game.start()
