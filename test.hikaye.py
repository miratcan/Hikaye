from hikaye import Game
from hikaye import PlaceContainer
from hikaye import Place
from hikaye import NORTH

places = PlaceContainer([
    Place(
        "Yatak Odasi",
        "Merhaba<<<<<<<Selamlar<<<<<<<<Yazacaklarım biraz uzun gelebilir."
        "< ama yine de bir yerden başlamak zorundayım. Bak, "
        "dün gece çok soguk<<<ğuktu. Rüzgarın suları donduracak soğukluğunu " \
        "kemiklerinde hissetmiştin<m. Üzerin<mdede<< de bir kazak ve soğuktan " \
        "koruyamayacak kadar ince bir de palton vardı. Üşümene aldırmadan " \
        "bir o sokaktan bir o sokağa gezip durmustun. Evlerde " \
        "yakılan kömürden çıkan pis havanın kokusunu en derinlerde " \
        "hissetmiştin. Evinin olduğu Sok<<<sokağın köşesine geldiğinde durdun. "
        "Gecenin karanlığını yok edip sokağı<<<<<<etrafı zar zor aydınlatan "
        "sokak lambasının altında son sigaranı içtin. Etrafta " \
        "kimseler görünmüyordu. Gün herkes için bitmişti, kendin için de "
        "bitmesini dilemekten başka da bir çaren yok gibi gözüküyordu. "
        "İlerden kavga eden iki kedinin bağrışmaları gelirken apartmana " \
        "girdin, yukarı çıktın. Yatağına yatıp pencereden gelen ay ışığına "
        "doğru bıraktın zihnini.\n\n"  \

        "Sabah uyandığında, güneş içini ısıtmaya başlamıştı çoktan."
        "Etrafın öylece bakıyordun\n\n" \

        "Burasi pek de modern olmayan esyalarla dosenmis. Karsinda bir " \
        "elbise dolabi sol tarafinda ise pencere var. Sag tarafta cekmeceli " \
        "baska bir dolap ve onun uzerinde duz bir ayna mevcut. Odanin ici " \
        "aydinlik. Pencereden gelen sari sicak isik gunun erken saatlerinde " \
        "oldugunu anlamana yetiyor."
    ),
    Place(
        "Koridor",
	"Biraz onceki aydinlik hal yok oldu. Burasi oldukca serin. " \
	"Sag tarafta calisma odasinin girisi mecvut. Sol tarafta ise misafir " \
        "yatak odasinin girisi."
    )
])

places.connect('Yatak Odasi', NORTH, 'Koridor')

game = Game('Depremden Kurtul', author='Mirat Can Bayrak', places=places)

game.player.place = game.places.get('Yatak Odasi')

game.start()
input('Ne yapmak istiyorsun?')
