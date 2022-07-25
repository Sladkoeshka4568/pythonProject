import aiohttp
import asyncio
from fake_useragent import UserAgent
import math
import json
import requests


ua = UserAgent()



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
    page = []
    date_kufar = []
    date_id = []
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
            # !!!!!!! переписать, ошибки по колличеству комнат
            item_url = i.get('ad_link')
            item_last_time_up = i.get('list_time')

            # response_phone = requests.get(
            #     url=f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/item/{item_id}/phone',
            #     headers={'user-agent': f'{ua.random}'}).json()
            # item_phone = response_phone.get('phone')
            date_id.append({
                'id': item_id
            })
            date_kufar.append({
                'id': item_id,
                'price': items_price_usd,
                'location': item_location,
                'rooms': item_rooms,
                'ulr': item_url,
                # 'phone': item_phone,
                'last_time_up': item_last_time_up
            })
            print(f'Sparsily {len(date_kufar)} out of {total_apartments}')

    with open('result_kufar.json', 'w',encoding='utf-8') as file:
        json.dump(date_kufar, file, indent=4, ensure_ascii=False)
    return date_id







async def main():
    async with aiohttp.ClientSession() as session:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': f'{ua.random}'
        }
        app_id = collect_data_kufar()
        tasks = []  # Создаем массив, куда будем помещать задания
        for i in app_id:
            tasks.append(parsing_page(session,
                                        f'https://lolz.guru/articles/{nextpageurl}{i}'))  # Передаем в другую функцию сессию, а так же ссылку на парсинг

        asyncio.gather(*tasks)  # Выполняем то, что находится в массиве

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

