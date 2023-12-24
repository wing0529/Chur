import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

def load_training_data(file_path='output_data.csv'):
    try:
        df = pd.read_csv(file_path)

        # 특성(X_train)과 레이블(y_train)을 추출
        X_train = df[['R', 'G', 'B']]  # 특성'R', 'G', 'B' 
        y_train = df['judge']  # 레이블 'judge'

        return X_train, y_train

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None, None

def extract_central_rgb(image_path):
    image = Image.open(image_path)
    width, height = image.size
    central_pixel = image.getpixel((width // 2, height // 2))
    return central_pixel

def load_images_from_folder(folder_path):
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg'):
            image_paths.append(os.path.join(folder_path, filename))
    return image_paths

folder_path = "/home/pi/Park-main"
image_paths = load_images_from_folder(folder_path)

data = []

for image_path in image_paths:
    # 중앙 부분의 RGB 값을 추출
    rgb = extract_central_rgb(image_path)
    data.append(rgb)

# Extracting data for plotting
R_values = [item[0] for item in data]
G_values = [item[1] for item in data]
B_values = [item[2] for item in data]

# 훈련 데이터 불러오기
X_train, y_train = load_training_data()

# 특성 스케일링을 위한 RobustScaler를 초기화.
rbs = RobustScaler()

# 훈련 데이터에 대해 RobustScaler를 적용
X_train_robust = rbs.fit_transform(X_train)

# SVM 모델을 초기화
loaded_model = joblib.load('best_svm.joblib')

# 새로운 데이터에 대한 예측을 위해 데이터를 가공
new_data = pd.DataFrame({'R': R_values, 'G': G_values, 'B': B_values})
new_data_robust = rbs.transform(new_data)

# SVM 모델을 사용하여 'judge'를 예측
prediction = loaded_model.predict(new_data_robust)
print("Prediction result (judge):", prediction[0])

#txt파일로 내보내기
prediction_result = loaded_model.predict(new_data_robust)
output_file_path='predicted_judge.txt'
with open(output_file_path, 'w') as output_file:
    for value in prediction_result:
        output_file.write(str(value) + '\n')