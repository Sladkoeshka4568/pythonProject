from fake_useragent import UserAgent
import requests
import json
from bs4 import BeautifulSoup
import math




ua = UserAgent()


def collect_data_onliner():
    response = requests.get(
        url='https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type[]=1_room&rent_type[]=2_rooms&rent_type[]=3_rooms&rent_type[]=4_rooms&rent_type[]=5_rooms&rent_type[]=6_rooms&only_owner=true',
        headers={'user-agent': f'{ua.random}'})
    # нашли последнюю страницу
    tmp = response.json()
    last = tmp.get('page').get('last')
    total = int(tmp.get('total'))




    count = 0
    data_onliner = []
    for item in range(1, int(last) + 1):

        url = f'https://r.onliner.by/sdapi/ak.api/search/apartments?rent_type[]=1_room&rent_type[]=2_rooms&rent_type[]=3_rooms&rent_type[]=4_rooms&rent_type[]=5_rooms&rent_type[]=6_rooms&only_owner=true&page={item}'
        response = requests.get(
            url=url,
            headers={'user-agent': f'{ua.random}'})

        data = response.json()
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

            data_onliner.append({
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
            print(f'Sparsily {len(data_onliner)} out of {total}')

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data_onliner, file, indent=4, ensure_ascii=False)




def collect_data_kufar():
    response = requests.get(
        url='https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cmp=0&cur=USD&gbx=b%3A20.561200890624985%2C51.41464455654549%2C34.865400109374974%2C55.45222546814571&gtsy=country-belarus&lang=ru&rnt=1&size=200&typ=let',
        headers={'user-agent': f'{ua.random}'}).json()

    total_apartments = response.get('total')
    total_page = math.ceil(total_apartments/200)
    def search_next_page(response):
        search_next_page = response.get('pagination').get('pages')
        for i in search_next_page:
            if i['label'] == "next":
                page = i['token']
                return '&cursor=' + page
    date_kufar = []
    page = []
    for i in range(1, total_page+1):

        response = requests.get(
            url=f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cmp=0&cur=USD{page}&gbx=b%3A20.39785989062499%2C51.627623704913894%2C34.70205910937501%2C55.64576960781322&gtsy=country-belarus&lang=ru&rnt=1&size=200&typ=let',
            headers={'user-agent': f'{ua.random}'}).json()

        page = search_next_page(response)

        items = response.get('ads')
        for i in items:
            item_id = i.get('ad_id')
            items_price_usd = int(i.get('price_usd'))/100
            item_location = i.get('account_parameters')[1].get('v')
            # item_lat = i.get('ad_parameters')[0].get('v')
            # item_log
            item_rooms = i.get('ad_parameters')[6].get('v')
            item_url = i.get('ad_link')
            item_last_time_up = i.get('list_time')

            response_phone = requests.get(
                url=f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/item/{item_id}/phone',
                headers={'user-agent': f'{ua.random}'}).json()
            item_phone = response_phone.get('phone')

            date_kufar.append({
                'id': item_id,
                'price': items_price_usd,
                'location': item_location,
                'rooms': item_rooms,
                'ulr': item_url,
                'phone': item_phone,
                'last_time_up': item_last_time_up
            })
            print(f'Sparsily {len(date_kufar)} out of {total_apartments}')







    with open('result_kufar.json', 'w',encoding='utf-8') as file:
        json.dump(date_kufar, file, indent=4, ensure_ascii=False)



def main():
    # collect_data_onliner()
    collect_data_kufar()



if __name__ == '__main__':
    main()