from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# 저장된 모델과 scaler 로드
with open('model_2.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# 주가 예측을 위한 경로 및 함수
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 웹페이지에서 입력된 데이터 받기
    closing_price = float(request.form['closing_price'])

    # 입력 데이터 전처리 및 예측
    input_data = preprocess_data(closing_price)
    input_data = np.array(input_data).reshape(1, -1)
    input_data = scaler.transform(input_data)  # 스케일링 적용
    result = loaded_model.predict(input_data)
    prediction = scaler.inverse_transform(result)  # 스케일링 복원

    # 예측 결과 반환
    return render_template('index.html', prediction=prediction[0])

# 데이터 전처리 함수
def preprocess_data(closing_price):
    # 종가 데이터를 입력으로 받아 전처리 작업을 수행하는 함수

    # 스케일링을 위한 최소값과 최대값 설정
    min_value = 0
    max_value = 100000

    # 입력 데이터를 스케일링
    #scaled_data = (closing_price - min_value) / (max_value - min_value)
    scaled_data = scaler.transform([[closing_price]])  # 스케일링 적용
    # 추가적인 전처리 작업 수행
    # ...

    # 전처리된 데이터 반환
    return scaled_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
