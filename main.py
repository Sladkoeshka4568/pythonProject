from fake_useragent import UserAgent
import requests
import json
from bs4 import BeautifulSoup



ua = UserAgent()


def collect_data_onliner():
    response = requests.get(
        url=f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type[]=1_room&rent_type[]=2_rooms&rent_type[]=3_rooms&rent_type[]=4_rooms&rent_type[]=5_rooms&rent_type[]=6_rooms&only_owner=true',
        headers={'user-agent': f'{ua.random}'})
    # нашли последнюю страницу
    tmp = response.json()
    last = tmp.get('page').get('last')
    tmp_date = []

    count = 0
    data_hata = []
    for item in range(1, int(last) + 1):
        url = f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type[]=1_room&rent_type[]=2_rooms&rent_type[]=3_rooms&rent_type[]=4_rooms&rent_type[]=5_rooms&rent_type[]=6_rooms&only_owner=true&page={item}'
        response = requests.get(
            url=url,
            headers={'user-agent': f'{ua.random}'})

        data = response.json()
        tmp_date.append(data)
        items = data.get('apartments')

        for i in items:
            count += 1
            items_id = i.get('id')

            items_price_usd = i.get('price').get('amount')

            items_location = i.get('location')
            items_lat = items_location['latitude']
            items_log = items_location['longitude']
            items_location = items_location['address']

            items_rooms = i.get('rent_type')[0]

            items_url = i.get('url')

            items_created_at = i.get('created_at')
            items_last_time_up = i.get('last_time_up')

            response_tel = requests.get(url=items_url, headers={'user-agent': f'{ua.random}'})
            soup_tel = response_tel.text
            soup = BeautifulSoup(soup_tel, "html.parser")
            try:
                phone = soup.find('div', id='apartment-phones').find('a').text

            except AttributeError:
                response_tel = requests.get(url=items_url, headers={'user-agent': f'{ua.random}'})
                soup_tel = response_tel.text
                soup = BeautifulSoup(soup_tel, "html.parser")
                phone = soup.find('div', id='apartment-phones').find('a').text
            print(items_url)
            print(phone)

            data_hata.append({
                    'num': count,
                    'id': items_id,
                    'price': items_price_usd,
                    'location': items_location,
                    'rooms': items_rooms,
                    'url': items_url,
                    'phone': phone,
                    'lat': items_lat,
                    'log': items_log,
                    'created_at': items_created_at,
                    'last_time_up': items_last_time_up})
            print(len(data_hata))

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data_hata, file, indent=4, ensure_ascii=False)

    with open('tmp.json', 'w', encoding='utf-8') as file:
        json.dump(tmp_date, file, indent=4, ensure_ascii=False)


# def collect_data_kufar():
#     response = requests.get(
#         url=f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type[]=1_room&rent_type[]=2_rooms&rent_type[]=3_rooms&rent_type[]=4_rooms&rent_type[]=5_rooms&rent_type[]=6_rooms&only_owner=true',
#         headers={'user-agent': f'{ua.random}'})
#     # нашли последнюю страницу
#     tmp = response.json()
#     last = tmp.get('page').get('last')
#
#
#     data_hata = []
#     for item in range(1, int(last) + 1):
#         url = f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type[]=1_room&rent_type[]=2_rooms&rent_type[]=3_rooms&rent_type[]=4_rooms&rent_type[]=5_rooms&rent_type[]=6_rooms&only_owner=true&page={item}'
#         response = requests.get(
#             url=url,
#             headers={'user-agent': f'{ua.random}'})
#
#         data = response.json()
#         items = data.get('apartments')
#         for i in items:
#             items_id = i.get('id')
#
#             items_price_usd = i.get('price').get('amount')
#             print(items_price_usd)
#             # items_price_usd = items_price_usd['converted']['USD']['amount']
#
#             items_location = i.get('location')
#             items_lat = items_location['latitude']
#             items_log = items_location['longitude']
#             items_location = items_location['address']
#
#             items_rooms = i.get('rent_type')[0]
#
#             # items_rooms = items_rooms[0]
#
#             items_url = i.get('url')
#
#             items_created_at = i.get('created_at')
#             items_last_time_up = i.get('last_time_up')
#
#             data_hata.append({
#                     'id': items_id,
#                     'price': items_price_usd,
#                     'location': items_location,
#                     'rooms': items_rooms,
#                     'url': items_url,
#                     # 'phone': telephon,
#                     'lat': items_lat,
#                     'log': items_log,
#                     'created_at': items_created_at,
#                     'last_time_up': items_last_time_up})
#             print(len(data_hata))
#
#     with open('result.json', 'w') as file:
#         json.dump(data_hata, file, indent=4, ensure_ascii=False)

def main():
    collect_data_onliner()



if __name__ == '__main__':
    main()