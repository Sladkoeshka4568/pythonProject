import requests
import json
from fake_useragent import UserAgent
import datetime


dt = datetime.datetime.now().strftime('%d-%m-%Y_%H;%M;%S')
ua = UserAgent()




def get_data():
    data_miners = []
    headers = {
        'User-Agent': f'{ua.random}',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://moonarch.app/',
        'Version': '2.13.1',
        'Origin': 'https://moonarch.app',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'If-None-Match': 'W/339de-L2gyEdk7994SFr7BKvh1PIYJtX4',
    }

    params = {
        'full': '1',
    }

    response = requests.get('https://api.moonarch.app/1.0/miners/list', params=params, headers=headers).json()
    for item in response.get('miners'):
        mining_group = item.get('name')
        print(mining_group)
    #
    #
    #
        # data_miners.append({
        #     'mining_group': mining_group
        # })

    # with open(f'result_for_{dt}.json', 'w', encoding='utf-8') as file:
    #     json.dump(response, file, indent=4, ensure_ascii=False)

def main():
    get_data()


if __name__ == '__main__':
    main()
