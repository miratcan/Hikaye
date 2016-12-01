# Hikaye

Hikaye, metin tabanlı etkileşimli hikayeler yazmak amacıyla oluşturulmuş bir
betik dilidir. Bu belge de Hikaye dilinin belirtecidir ve henüz taslak 
aşamasındadır.

Son Güncellenme: 27-11-2016 

## Ana Bloklar:

Bir oyunu oluşturabilmek için oyunla ilgili çeşitli nesneleri ve etkileşimleri 
tanımlamamız gerekmektedir. Ana bloklar yaptığımız tanımlamarı tiplerine göre 
gruplamamızı sağlar. Bir hikaye dosyasında Ana Bloklar ortalama aşağıdaki gibi 
gözükecektir.

    --- Hikaye ---


    ...
    ...


    --- Nesneler ---


    ...
    ...


    --- Karakterler ---


    ...
    ...


    --- Mekanlar ---

    ...
    ...
 

Örneğin eğer elimizde "Yaşlı Adam" adında bir karakter varsa bunu 
"Karakterler" ana bloğu altında, "Telefon" adında bir nesne varsa da 
"Nesneler" bloğu altında tanımlayabiliriz. Bu sayede çalıştırıcımız ona 
gösterdiğimiz nesnelerin tipini algılar.

Ana bloklar tanımlanırken üstünde ve altında iki adet boşluk bırakılır.


## Nesneler:


Nesneler ilgili Ana Bloğun altında tanımlanır. Örneğin elimizde "Yaşlı Adam"
adında bir karakter var. Bunu aşağıdaki gibi tanımlarız.

    --- Hikaye ---

    ...
    ...


    --- Karakterler ---


    Yaşlı Adam:

        İncelendiğinde: Buruşmuş yüzü ve eksik dişleriyle bana bakıyor,
        karanlık gözleri sanki bir şey anlatmaya çalışıyordu.


    --- Mekanlar ---


    ...
    ...

Nesneler "Nesne İsmi:" şeklinde isimlendirilerek tanımlanır. Nesnenin tipi
içinde bulunduğu Ana Blok tarafından belirlenir. Nesnelere ait özellikler de
Özellik: şeklinde ve 4 karakter girintilenerek yazılır. Bu örnekte bir
"Yaşlı Adam" karakteri, ve bu karakter incelendiğinde ortaya çıkacak yazı
belirlenmiştir.

## Özellikler

Nesnelere ait özellikler nesne tanımlamarının altına 4 karakter girintilenerek
yapılır. Özelliklere verilen değerlerin cinsi çalıştırıcı tarafından otomatik
olarak algılanır. Eğer girilen değer 79 karakterden uzunsa bir alt satırdan
aynı girintileme ile devam edilir.

## Veri Tipleri

Özelliklere verilen değerlerin tipleri otomatik olarak algılanır. Hikaye
dilinde var olan veri tipleri şunlardır:

  * Metin
  * Sayı
  * Ondalıklı Sayı
  * Referans
  * Fonksiyon


Aşağıdaki örnekte var olan bütün veri tiplerini görebilirsiniz:



    --- Hikaye --- 

    ...
    ...

    --- Nesneler ---

    ...
    ...

    --- Karakterler ---

    Yaşlı Adam:

        İncelendiğinde: Buruşmuş yüzü ve eksik dişleriyle bana bakıyor,
        karanlık gözleri sanki bir şey anlatmaya çalışıyordu.

        Birden bire ortaya çıkmıştı nereden geldiğini görememiştim.

        Maharet: 10
      
        Pi Sayısı: 3.14
      
        Taşıdıkları: $Saat


        


