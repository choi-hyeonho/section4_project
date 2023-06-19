import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

def parse_page(code, start_page, end_page):
    data_frames = []

    for page in range(start_page, end_page + 1):
        url = f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        response = requests.get(url=url, headers={'User-Agent': agent})
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table")
        if table is not None:
            df = pd.read_html(str(table), header=0)[0]
            df = df.dropna()
            data_frames.append(df)
        else:
            print("테이블을 찾지 못했습니다.")

    if data_frames:
        merged_df = pd.concat(data_frames, ignore_index=True)
        return merged_df
    else:
        print("데이터를 가져올 수 없습니다.")
        return None

code = '005930'  # 주식 코드
start_page = 1  # 시작 페이지
end_page = 50  # 종료 페이지
data = parse_page(code, start_page, end_page)

data = data.sort_values('날짜')
data = data.dropna()
data = data.drop_duplicates()

# MongoDB 연결 정보 설정
HOST = 'cluster0.zycseoh.mongodb.net'
USER = 'maesil1115'
PASSWORD = 'gusgh12'
DATABASE_NAME = 'cluster0'
COLLECTION_NAME = 'samsung_stock'  # 변경된 컬렉션 이름
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

# MongoDB 연결
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# 데이터프레임을 MongoDB 컬렉션에 적재
data_dict = data.to_dict('records')
collection.insert_many(data_dict)

# 연결 종료
client.close()

