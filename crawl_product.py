from curl_cffi import requests
import time
import random
import pandas as pd

session = requests.Session(impersonate="chrome120")

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/sach-truyen-tieng-viet/c316',
}

params = {
    'limit': '10',
    'sort': 'top_seller',
    'page': '1',
    'urlKey':  'sach-truyen-tieng-viet',
    'category': '316',
}

product = []
for i in range(1, 11):
    params['page'] = i
    response = session.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get('data', [])
        print(f'Page {i} request success!!! Found {len(items)}')
        for record in items:
            product.append({
                'id': record.get('id'),
                'name': record.get('name')
            })
            
    else:
        print(f'Failed at page {i} - Status Code: {response.status_code}')
        print(response.text)
    time.sleep(random.randrange(3, 10))
    

df = pd.DataFrame(product)
df.to_csv('product.csv', index=False)
