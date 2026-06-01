from curl_cffi import requests
import pandas as pd
import time
import random
from tqdm import tqdm
import concurrent.futures
import os


session = requests.Session(impersonate="chrome120")

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://tiki.vn/',
}

def comment_parser(json_data):
    d = dict()
    d['id'] = json_data.get('id') 
    d['product_id'] = json_data.get('product_id')
    d['content'] = json_data.get('content')
    d['customer_id'] = json_data.get('customer_id')
    d['rating'] = json_data.get('rating')
    return d

def fetch_single_page(pid, page):
    params = {
        'product_id': str(pid),
        'sort': 'score|desc,id|desc,stars|all',
        'page': str(page),
        'limit': '5',
        'include': 'comments,contribute_info,attribute_vote_summary'
    }
    try:
        response = session.get('https://tiki.vn/api/v2/reviews', headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    return None

def scrape_product_reviews(pid):
    all_comments = []
    
    first_page_data = fetch_single_page(pid, 1)
    if not first_page_data or not first_page_data.get('data'):
        return []
    
    for comment in first_page_data.get('data', []):
        content = comment.get('content')
        if content and str(content).strip() != "":
            all_comments.append(comment_parser(comment))
        
    paging_info = first_page_data.get('paging', {})
    last_page = paging_info.get('last_page', 1)
    
    if last_page > 1:
        max_threads = 5  
        pages_to_fetch = range(2, last_page + 1)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {executor.submit(fetch_single_page, pid, page): page for page in pages_to_fetch}
            
            for future in concurrent.futures.as_completed(futures):
                page_result = future.result()
                if page_result and page_result.get('data'):
                    for comment in page_result.get('data'):
                        content = comment.get('content')
                        if content and str(content).strip() != "":
                            all_comments.append(comment_parser(comment))
                        
                time.sleep(random.uniform(0.1, 0.4))
                
    return all_comments

if __name__ == "__main__":
    df_id = pd.read_csv('Tiki_crawlData/product.csv')
    p_ids = df_id['id'].dropna().drop_duplicates().to_list()

    csv_filename = 'Tiki_crawlData/fast_comments_filtered.csv'

    for pid in tqdm(p_ids, total=len(p_ids), desc="Progress"):
        product_comments = scrape_product_reviews(pid)
        
        if product_comments:
            df_temp = pd.DataFrame(product_comments)
            
            df_temp.to_csv(
                csv_filename, 
                mode='a', 
                index=False, 
                header=not os.path.exists(csv_filename),
                encoding='utf-8-sig'
            )
            
        time.sleep(random.uniform(2, 4))

