import requests
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/005930.KS/history?p=005930.KS"

# URL에서 페이지 내용 가져오기
response = requests.get(url)
html_content = response.text

# BeautifulSoup을 사용하여 HTML 파싱
#soup = BeautifulSoup(html_content, "html.parser")
soup = BeautifulSoup(html_content, "lxml")

# 주식 데이터가 있는 테이블 요소 선택
#table = soup.find("table", class_="W(100%) M(0)")
table = soup.select_one("table.W\(100\%\).M\(0\)")

# 테이블 행(tr)을 순회하며 데이터 추출
for row in table.find_all("tr"):
    # 각 행의 셀(td)을 가져와서 출력 또는 처리
    cells = row.find_all("td")
    if len(cells) >= 7:
        date = cells[0].text
        open_price = cells[1].text
        high_price = cells[2].text
        low_price = cells[3].text
        close_price = cells[4].text
        adj_close_price = cells[5].text
        volume = cells[6].text

        # 데이터 출력 또는 원하는 처리 수행
        print("Date:", date)
        print("Open:", open_price)
        print("High:", high_price)
        print("Low:", low_price)
        print("Close:", close_price)
        print("Adj Close:", adj_close_price)
        print("Volume:", volume)
        print("------------------------")
