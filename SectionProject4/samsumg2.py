import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
from sqlalchemy import create_engine

url = 'https://finance.naver.com//item/sise_day.naver?code=005930'
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
response = requests.get(url, headers={'User-Agent': agent})
soup = BeautifulSoup(response.text, 'lxml')
print(response.status_code)
print()

def parse_page(code, start_page, end_page):
    try:
        data_frames = []  # 각 페이지의 데이터프레임을 저장할 리스트

        for page in range(start_page, end_page+1):
            url = 'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
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
    except:
        traceback.print_exc()
    return None

code = '005930'  # 주식 코드
start_page = 1  # 시작 페이지
end_page = 50  # 종료 페이지
data = parse_page(code, start_page, end_page)
#print(data)

data = data.sort_values('날짜')

data = data.dropna()  # 결측치 제거 (추가)
data = data.drop_duplicates()  # 중복값 제거 (추가)

print(data)

import psycopg2
#from sqlalchemy import create_engine

# ElephantSQL 연결 정보 설정
host = 'drona.db.elephantsql.com'
user = 'ctmplful'
password = 'gv2Zhl5SuyL7TN0WZTugN-yTcz86FwGC'
database = 'ctmplful'

# ElephantSQL 연결
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
connection = engine.connect()

# 데이터프레임을 ElephantSQL 테이블에 적재
table_name = 'stock_data'  # 테이블명
data.to_sql(name=table_name, con=connection, if_exists='replace', index=False)

# 연결 종료
connection.close()

print(type(data))