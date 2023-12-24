from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
from threading import Thread


app = Flask(__name__)
socketio = SocketIO(app)

# 초기 값 설정
current_value = 'safe'
def generate_random_value():
 #   global current_value
    while True:
        # 0에서 10 사이의 랜덤 값 생성
        #파일에서 텍스트 읽어와서 변수에 저장
        with open("/home/pi/Park-main/predicted_judge.txt","r") as file:
            current_value = file.read().strip()
            print("Current Value:",current_value)
            socketio.emit('update_value', {'value': current_value})
            time.sleep(1)
            
        # 웹 소켓을 통해 클라이언트에게 값 전송
        

@app.route('/')
def first1():
    return render_template('first1.html')

@app.route('/second.html')
def second():
    return render_template('second.html')

@app.route('/fourth.html')
def fourth():
    return render_template('fourth.html')

@app.route('/index.html')
def index():   
    return render_template('index.html',initial_value=current_value)

@app.route('/seventh.html')
def seventh():
    return render_template('seventh.html')

@app.route('/fifth2.html')
def fifth2():
    return render_template('fifth2.html')

@app.route('/eleventh.html')
def eleventh():
    return render_template('eleventh.html')

@app.route('/Guide.html')
def Guide():
    return render_template('Guide.html')

@app.route('/when.html')
def when():
    return render_template('when.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    # 백그라운드에서 랜덤 값 생성 및 전송을 수행할 스레드 시작
    #generator_thread = Thread(target=generate_random_value)
    #generator_thread.daemon = True
    #generator_thread.start()
    thread = Thread(target=generate_random_value)
    thread.daemon = True
    thread.start()

    # Flask 애플리케이션 실행
    socketio.run(app, host='0.0.0.0', port=5000,debug=True)
