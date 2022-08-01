import aiohttp
import asyncio
from fake_useragent import UserAgent
import math
import json
import requests
from bs4 import BeautifulSoup


# https://lolz.guru/threads/3008577/

ua = UserAgent()
data = []


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
            date_id.append(item_id)
            date_kufar.append({
                'id': item_id,
                'price': items_price_usd,
                'location': item_location,
                'rooms': item_rooms,
                'ulr': item_url,
                # 'phone': item_phone,
                'last_time_up': item_last_time_up
            })

    with open('result_kufar.json', 'w',encoding='utf-8') as file:
        json.dump(date_kufar, file, indent=4, ensure_ascii=False)
    return date_id



async def get_phone(session, phone_id):
    headers = {
        'User-Agent': f'{ua.random}'
        }
    proxies = {
        'https': 'http://178.254.24.12:3128'
    }
        # 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Connection': 'keep-alive',
        # # Requests sorts cookies= alphabetically
        # # 'Cookie': 'lang=ru; kuf_VCH_promo_vas=2; kuf-searchbar-only-title=1; web_push_banner_listings=3; _ga=GA1.2.842914772.1659097777; _pulse2data=0a2d752f-e516-4b9f-bfe7-048b4947879f%2Cv%2C%2C1659103399622%2CeyJpc3N1ZWRBdCI6IjIwMjItMDctMjlUMTI6Mjk6MzVaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..z5F_oNJ_TEE3MmacuRiaXA.2B352U4kC7CDnebQFnIohM1H09N1t7VsUvWFGT0fncXNfKTMe_ArziH0B2Mzavlas8jFwOrJrZZSHTf8BG_oAQSaITj5uSNcCTZ_tJ2jy8E_9sJRg00-2Fuzh4UvFhJal67iziB5ceJQ-g7KRLrPAFPJYBq82gmB2d6HQTV1a1oFhnihghGZJKc0gE89xMLViQkxK0DyYc3uoE-h6zB22Q.xJADWal_IwyozBCu3lQL5g%2C0%2C1659116899622%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..1ilt8kc4cWoT6SCJYaZebV_NU1ZMidQ2tdnmK1KWbv4; kuf_agr={%22advertisements%22:true%2C%22statistic%22:true%2C%22mindbox%22:true}; fullscreen_cookie=1; kuf_SA_vas_adv_game_2022_popup=1; _gcl_au=1.1.1859754093.1659097780; _ga_QTFZM0D0BE=GS1.1.1659097779.1.0.1659097781.58; tmr_reqNum=16; tmr_lvid=d424eccb1ab1ed30aeed5a43123f531c; tmr_lvidTS=1659097780524; _tt_enable_cookie=1; _ttp=e9eeea42-0bcf-49ee-8aed-f6c1d2a89b2b; web_push_banner_realty=3; _ga_SW9X2V65F0=GS1.1.1659102501.2.1.1659102984.0; _ym_uid=16590977841073363313; _ym_d=1659097784; mindboxDeviceUUID=fe678108-b60c-4c06-8201-68bb6deee9a5; directCrm-session=%7B%22deviceGuid%22%3A%22fe678108-b60c-4c06-8201-68bb6deee9a5%22%7D; _hjSessionUser_1751529=eyJpZCI6IjIwM2FjMzY2LWFlMTItNTZmNS04ZTQxLWEwYjdmMmY0MTgzZSIsImNyZWF0ZWQiOjE2NTkwOTc3ODQzMDIsImV4aXN0aW5nIjp0cnVlfQ==; default_ya=240; default_ca=7; kuf_SA_subscribe_user_attention=1',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
        # # Requests doesn't support trailers
        # # 'TE': 'trailers',
    # }

    url = f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/item/{phone_id}/phone'
    async with session.get(url=url, headers=headers, proxies=proxies) as response:
        response_text = await response.text()
        print(response_text)
        data.append({phone_id: response_text})


async def task_list():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for phone_id in collect_data_kufar():
            task = asyncio.create_task(get_phone(session, phone_id))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    asyncio.run(task_list())

    with open('resulr_kufar_phone.json', "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()






