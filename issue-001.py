import json
import keyword
import pytest


class ColorizeMixin:

    def color_text(self, repr_color):
        print('\033[1;' + repr_color + ';10m')


class Advert(ColorizeMixin):

    def __init__(self, mapping):
        self.repr_color = '36'
        self.title = mapping['title']
        self.location = self
        super().__init__()
        for i in mapping:
            if i == 'location':
                for j in mapping[i]:
                    self.location.__dict__[j] = mapping[i][j]
            elif keyword.iskeyword(i):
                k = i + '_'
                self.__dict__.__setitem__(k, mapping[i])
            else:
                self.__dict__.__setitem__(i, mapping[i])

            if i == 'price' and mapping[i] < 0:
                raise ValueError('price must be >= 0')
            elif not 'price' in self.__dict__:
                self.__dict__['price'] = 0

    def __repr__(self):
        super().color_text(self.repr_color)
        return f'{self.title} | {self.price} ₽'


@pytest.mark.parametrize('adv1, adv_ad', [("""
    {"title": "Вельш-корги",
      "price": 1000,
      "class": "dogs",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }""", """Вельш-корги | 1000 ₽""")])
def test_decode_01(adv1, adv_ad):
    assert str(Advert(json.loads(adv1))) == adv_ad


@pytest.mark.parametrize('adv1, adv_ad', [("""
    {"title": "Котик",
      "price": 2000,
      "class": "cats",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }""", """Котик | 2000 ₽""")])
def test_decode_02(adv1, adv_ad):
    assert str(Advert(json.loads(adv1))) == adv_ad


@pytest.mark.parametrize('adv1, adv_ad', [("""
    {"title": "python",
      "price": 1500,
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }""", """python | 1500 ₽""")])
def test_decode_03(adv1, adv_ad):
    assert str(Advert(json.loads(adv1))) == adv_ad


lesson_str = """{
    "title": "python",
    "price": 1000,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
    }"""
corgi_str = """{
      "title": "Вельш-корги",
      "price": 1000,
      "class": "dogs",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }"""
corgi = json.loads(lesson_str)
corgi_ad = Advert(corgi)
print(corgi_ad)
# print(corgi_ad.title)
# print(corgi_ad.price)
# print(corgi_ad.class_)
# print(corgi_ad.location.metro_stations)
# print(corgi_ad.location.address)
adv = """{
      "title": "Вельш-корги",
      "price": 1000,
      "class": "dogs",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }"""
# print(Advert(json.loads(adv)))