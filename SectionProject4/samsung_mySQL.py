import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
from sqlalchemy import create_engine
import pymysql

def parse_page(code, start_page, end_page):
    try:
        data_frames = []

        for page in range(start_page, end_page + 1):
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

data = data.sort_values('날짜')

data = data.dropna()
data = data.drop_duplicates()

host = '127.0.0.1'
user = 'root'
password = '1234'
database = 'project4'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
connection = engine.connect()

table_name = 'stock_data'
data.to_sql(name=table_name, con=connection, if_exists='replace', index=False)

connection.close()
