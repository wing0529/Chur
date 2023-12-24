import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import joblib

def extract_central_rgb(image_path):
    image = Image.open(image_path)
    width, height = image.size
    central_pixel = image.getpixel((width // 2, height // 2))
    return central_pixel

def load_images_from_folder(folder_path,keyword):
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') and filename.startswith(keyword):
            image_paths.append(os.path.join(folder_path, filename))
    return image_paths

keyword ='fixed'
folder_path = "/home/pi/Desktop/final/total"
image_paths = load_images_from_folder(folder_path,keyword)

data = []

for image_path in image_paths:
    judge_value = 'error'
    # 이미지 파일 제목에서 pH 추출
    pH_value = os.path.splitext(os.path.basename(image_path))[0].split('_')[2]
    if (4.8<=float(pH_value)<=5.6):
        judge_value = 'danger'
    elif (5.7<=float(pH_value)<=6.0):
        judge_value = 'warning'
    elif (6.1<=float(pH_value)<=6.4):
        judge_value = 'safe'
        
    # 중앙 부분의 RGB 값을 추출
    rgb = extract_central_rgb(image_path)
    
    # 튜플로 데이터 생성
    image_data = (judge_value, pH_value, rgb[0], rgb[1], rgb[2])
    
    # 데이터 추가
    data.append(image_data)

# Extracting data for plotting
judge_values = [item[0] for item in data]
pH_values = [item[1] for item in data]
R_values = [item[2] for item in data]
G_values = [item[3] for item in data]
B_values = [item[4] for item in data]
    
#data dataframe로 저장    
df = pd.DataFrame(data, columns=['judge','pH', 'R', 'G', 'B'])

# DataFrame을 Excel 파일로 저장
excel_filename = 'output_data.csv'
#df.to_excel(excel_filename, index=False)
df.to_csv(excel_filename, index=False)

df.isnull().sum()

pd.get_dummies(df['judge'])

# DataFrame을 섞습니다.
df_shuffled = shuffle(df, random_state=42)

# 데이터를 훈련, 검증, 테스트 세트로 나눕니다.
train_size = 0.6  # 훈련에 60% 할당
valid_size = 0.2  # 검증에 20% 할당, 나머지 20%는 테스트에 할당됩니다.

train, temp = train_test_split(df_shuffled, train_size=train_size, random_state=42)
valid, test = train_test_split(temp, test_size=valid_size / (1 - train_size), random_state=42)

# 각 세트에 대해 독립 변수 (X)와 종속 변수 (y)를 분리합니다.
X_train, y_train = train[['R', 'G', 'B']], train['judge']
X_valid, y_valid = valid[['R', 'G', 'B']], valid['judge']
X_test, y_test = test[['R', 'G', 'B']], test['judge']

# RobustScaler를 사용하여 데이터 정규화
rbs = RobustScaler()
X_train_robust = rbs.fit_transform(X_train)
X_test_robust = rbs.transform(X_test)
X_valid_robust = rbs.transform(X_valid) 

# SVM 모델 생성
svm = SVC(random_state=42)

# 탐색할 하이퍼파라미터 값들 지정
param_grid_svm = {
    'C': [40],
    'kernel': ['rbf'],
    'gamma': ['scale']
}

# GridSearchCV를 사용하여 하이퍼파라미터 튜닝
grid_search_svm = GridSearchCV(svm, param_grid_svm, cv=5)
grid_search_svm.fit(X_train_robust, y_train)

# 최적의 하이퍼파라미터 확인
best_params_svm = grid_search_svm.best_params_
'''print("최적의 하이퍼파라미터:", best_params_svm)'''

# 최적의 모델로 예측 수행
best_svm = grid_search_svm.best_estimator_
y_pred_tuned_svm = best_svm.predict(X_test_robust)

# 모델 저장
model_filename = 'best_svm.joblib'
joblib.dump(best_svm, model_filename)
print(f"모델이 {model_filename}로 저장되었습니다.")
