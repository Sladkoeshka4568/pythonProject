from fake_useragent import UserAgent
import requests
import json
from bs4 import BeautifulSoup

import math

data_station = {
    'Михалово': [53.87695100, 27.49708400],
    'Московская': [53.92797500, 27.62735000],
    'Институт_Культуры': [53.88523900, 27.53985800],
    'Борисовский_тракт': [53.93845600, 27.66579500],
    'Академия_Наук': [53.92161900, 27.59714400],
    'Уручье': [53.94583300, 27.68972200],
    'Петровщина': [53.86472200, 27.48611100],
    'Грушевка': [53.88666700, 27.51472200],
    'Октябрьская': [53.90166700, 27.56083300],
    'Восток': [53.934478, 27.651208],
    'Парк_Челюскинцев': [53.924165, 27.613378],
    'Площадь_Якуба_Колоса': [53.915836, 27.583279],
    'Площадь_Победы': [53.909471, 27.576204],
    'Площадь_Ленина': [53.892951, 27.547781],
    'Малиновка': [53.849966, 27.476893],
    
    'Пушкинская': [53.90944400, 27.49527800],
    'Кунцевщина': [53.90598200, 27.45244900],
    'Молодежная': [53.90638000, 27.52262900],
    'Пролетарская': [53.88961500, 27.58561800],
    'Первомайская': [53.89388900, 27.57027800],
    'Купаловская': [53.90170300, 27.56096100],
    'Спортивная': [53.90833300, 27.47916700],
    'Тракторный_завод': [53.88982500, 27.61505600],
    'Партизанская': [53.87459700, 27.63014400],
    'Немига': [53.90583300, 27.55388900],
    'Могилёвская': [53.86199400, 27.67430300],
    'Каменная_Горка': [53.90689200, 27.43751800],
    'Фрунзенская': [53.902496, 27.561481],
    'Автозаводская': [53.869305, 27.647657],


    'Юбилейная_площадь': [53.904411, 27.539984],
    'Площадь_Франтишка_Богушевича': [53.894942, 27.538035],
    'Вокзальная': [53.889773, 27.546893],
    'Кольварийская_слобода': [53.878851, 27.549568]

}


ua = UserAgent()

price_min = 200
price_max = 260
max_range = 1000
number_of_rooms = 1


def collect_data():
    response = requests.get(url=f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&price%5Bmin%5D={price_min}&price%5Bmax%5D={price_max}&currency=usd&only_owner=true&bounds%5Blb%5D%5Blat%5D=53.728230616071755&bounds%5Blb%5D%5Blong%5D=26.995792484592663&bounds%5Brt%5D%5Blat%5D=54.02775478792311&bounds%5Brt%5D%5Blong%5D=28.133926826987853&v=0.8656089621855964',
                             headers={'user-agent': f'{ua.random}'})
    # нашли последнюю страницу
    tmp = response.json()
    page = tmp.get('page')
    last = page['last']

    data_hata = []
    for item in range(1, int(last)+1):
        url = f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type%5B%5D={number_of_rooms}_room&price%5Bmin%5D={price_min}&price%5Bmax%5D={price_max}&currency=usd&only_owner=true&bounds%5Blb%5D%5Blat%5D=53.812409559871966&bounds%5Blb%5D%5Blong%5D=27.235107421875004&bounds%5Brt%5D%5Blat%5D=53.984357743019814&bounds%5Brt%5D%5Blong%5D=27.888793945312504&page=1&v=0.5020324252606277'
        response = requests.get(
            url=url,
            headers={'user-agent': f'{ua.random}'}
        )

        data = response.json()
        items = data.get('apartments')
        for i in items:
            items_id = i.get('id')

            items_price_usd = i.get('price')
            items_price_usd = items_price_usd['converted']['USD']['amount']

            items_location = i.get('location')
            items_lat = items_location['latitude']
            items_log = items_location['longitude']
            items_location = items_location['address']


            items_rooms = i.get('rent_type')
            items_rooms = items_rooms[0]

            items_url = i.get('url')


            response_tel = requests.get(url=items_url, headers={'user-agent': f'{ua.random}'})
            soup_tel = response_tel.text
            soup = BeautifulSoup(soup_tel, "lxml")
            try:
                telephon = soup.find('div', id='apartment-phones').find('a').text
            except AttributeError:
                telephon = soup.find('li', class_='apartment-info__item apartment-info__item_secondary')

            # добавляем расстояние до ближайшей станции метро
            nearest = {}
            rad = 6372795
            # координаты двух точек
            llat1 = items_lat
            llong1 = items_log
            for key, val in data_station.items():
                llat2 = val[0]
                llong2 = val[1]
                lat1 = llat1 * math.pi / 180.
                lat2 = llat2 * math.pi / 180.
                long1 = llong1 * math.pi / 180.
                long2 = llong2 * math.pi / 180.

                # косинусы и синусы широт и разницы долгот
                cl1 = math.cos(lat1)
                cl2 = math.cos(lat2)
                sl1 = math.sin(lat1)
                sl2 = math.sin(lat2)
                delta = long2 - long1
                cdelta = math.cos(delta)
                sdelta = math.sin(delta)

                # вычисления длины большого круга
                y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
                x = sl1 * sl2 + cl1 * cl2 * cdelta
                ad = math.atan2(y, x)
                dist = ad * rad

                nearest[int(dist)] = key

            print(telephon)
            tmp = min(nearest)
            if tmp <= max_range:
                data_hata.append(
                    {
                        'id': items_id,
                        'price': items_price_usd,
                        'location': items_location,
                        'rooms': items_rooms,
                        'url': items_url,
                        'phone': telephon,
                        'lat': items_lat,
                        'log': items_log,
                        'range_for': tmp,
                        'station': nearest[tmp]
                    }
                )
                print(len(data_hata))


    with open('result.json', 'w') as file:
        json.dump(data_hata, file, indent=4, ensure_ascii=False)





def main():
    collect_data()
    filter_pidar()



if __name__ == '__main__':
    main()



