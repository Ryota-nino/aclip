import os
import os.path
import sys
import cv2
import random
import json
import string
from typing import SupportsRound
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload
import schedule
import daemon
import subprocess
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, static_folder='./uploads/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remi.db'
db = SQLAlchemy(app)

sched = BackgroundScheduler(daemon=True)
sched.start()


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    image = db.Column(db.String(128), nullable=False)
    repeat_id = db.Column(db.String, default=0)
    flag = db.Column(db.Boolean, nullable=False, default=1)
    sound_id = db.Column(db.Integer, default=1)


class Repeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repeat_name = db.Column(db.String, nullable=False)


class Sound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sound_name = db.Column(db.String, nullable=False)


def startAlarm():
    print('アラーム開始')
    json_data = {"Value1": 2}
    headers = {'Content-Type': 'application/json'}
    requests.post(
        'https://maker.ifttt.com/trigger/start_alarm/with/key/ehsWG5yTpSDi6wmh7X20wWEiEWk4FoMLocB2hc1eLOh', data=json.dumps(json_data), headers=headers)

    # session['alarm'] = True

    return render_template('stop_alarm.html')


def stopAlarm():
    print('アラーム停止')
    requests.post(
        'https://maker.ifttt.com/trigger/stop_alarm/with/key/ehsWG5yTpSDi6wmh7X20wWEiEWk4FoMLocB2hc1eLOh')

    session.pop('alarm', None)


def imgRecognition(cascade_name, image_name):
    XML_PATH = "./data/cascade/" + cascade_name
    INPUT_IMG_PATH = "./" + image_name
    # OUTPUT_IMG_PATH = "output.png"

    classifier = cv2.CascadeClassifier(XML_PATH)
    img = cv2.imread(INPUT_IMG_PATH)
    color = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    targets = classifier.detectMultiScale(color)
    for x, y, w, h in targets:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # cv2.imwrite(OUTPUT_IMG_PATH, img)

    return True


def setAlarm(repeat_list, alarm):
    time = alarm.time.split(':')
    for repeat_id in repeat_list:
        if repeat_id == '1':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='mon', hour=str(time[0]), minute=str(time[1]), id='%s-mon' % alarm.id)
        elif repeat_id == '2':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='tue', hour=str(time[0]), minute=str(time[1]), id='%s-tue' % alarm.id)
        elif repeat_id == '3':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='wed', hour=str(time[0]), minute=str(time[1]), id='%s-wed' % alarm.id)
        elif repeat_id == '4':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='thu', hour=str(time[0]), minute=str(time[1]), id='%s-thu' % alarm.id)
        elif repeat_id == '5':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='fri', hour=str(time[0]), minute=str(time[1]), id='%s-fri' % alarm.id)
        elif repeat_id == '6':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='sat', hour=str(time[0]), minute=str(time[1]), id='%s-sat' % alarm.id)
        elif repeat_id == '7':
            sched.add_job(startAlarm, 'cron',
                          day_of_week='sun', hour=str(time[0]), minute=str(time[1]), id='%s-sun' % alarm.id)


def rescheduleAlarm(repeat_list, alarm):
    time = alarm.time.split(':')
    for repeat_id in repeat_list:
        if repeat_id == '1':
            print('enter')
            sched.reschedule_job(
                '%s-mon' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))
        elif repeat_id == '2':
            sched.reschedule_job(
                '%s-tue' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))
        elif repeat_id == '3':
            sched.reschedule_job(
                '%s-wed' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))
        elif repeat_id == '4':
            sched.reschedule_job(
                '%s-thu' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))
        elif repeat_id == '5':
            sched.reschedule_job(
                '%s-fri' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))
        elif repeat_id == '6':
            sched.reschedule_job(
                '%s-sat' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))
        elif repeat_id == '7':
            sched.reschedule_job(
                '%s-sun' % alarm.id, trigger='cron', hour=str(time[0]), minute=str(time[1]))


def removeAlarm(repeat_list, alarm):
    for repeat_id in repeat_list:
        if repeat_id == 1:
            sched.remove_job('%s-mon' % alarm.id)
        elif repeat_id == 2:
            sched.remove_job('%s-tue' % alarm.id)
        elif repeat_id == 3:
            sched.remove_job('%s-wed' % alarm.id)
        elif repeat_id == 4:
            sched.remove_job('%s-thu' % alarm.id)
        elif repeat_id == 5:
            sched.remove_job('%s-fri' % alarm.id)
        elif repeat_id == 6:
            sched.remove_job('%s-sat' % alarm.id)
        elif repeat_id == 7:
            sched.remove_job('%s-sun' % alarm.id)


def pauseAlarm(repeat_list, alarm):
    for repeat_id in repeat_list:
        if repeat_id == 1:
            sched.pause_job('%s-mon' % alarm.id)
        elif repeat_id == 2:
            sched.pause_job('%s-tue' % alarm.id)
        elif repeat_id == 3:
            sched.pause_job('%s-wed' % alarm.id)
        elif repeat_id == 4:
            sched.pause_job('%s-thu' % alarm.id)
        elif repeat_id == 5:
            sched.pause_job('%s-fri' % alarm.id)
        elif repeat_id == 6:
            sched.pause_job('%s-sat' % alarm.id)
        elif repeat_id == 7:
            sched.pause_job('%s-sun' % alarm.id)


def resumeAlarm(repeat_list, alarm):
    for repeat_id in repeat_list:
        if repeat_id == 1:
            sched.resume_job('%s-mon' % alarm.id)
        elif repeat_id == 2:
            sched.resume_job('%s-tue' % alarm.id)
        elif repeat_id == 3:
            sched.resume_job('%s-wed' % alarm.id)
        elif repeat_id == 4:
            sched.resume_job('%s-thu' % alarm.id)
        elif repeat_id == 5:
            sched.resume_job('%s-fri' % alarm.id)
        elif repeat_id == 6:
            sched.resume_job('%s-sat' % alarm.id)
        elif repeat_id == 7:
            sched.resume_job('%s-sun' % alarm.id)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        alarms = Alarm.query.all()
        repeats = Repeat.query.all()

        week_list = {"1": "月", "2": "火", "3": "水",
                     "4": "木", "5": "金", "6": "土", "7": "日"}

        # sched = BackgroundScheduler(daemon=True)
        # sched.add_job(startAlarm, 'cron',
        #               day_of_week='mon', hour='1', minute='19')
        # sched.start()
        sched = BackgroundScheduler(daemon=True)
        # setAlarm(sched)

        return render_template('index.html', alarms=alarms, repeats=repeats, week_list=week_list)
    else:
        time = request.form.get('time')
        app.logger.debug(request.form.get('image'))
        image_path = '.' + request.form.get('image_path')
        repeat_list = request.form.getlist('repeat')
        sound = request.form.get('sound')

        # 繰り返しの保存
        str_id = ""

        for repeat_id in repeat_list:
            str_id = str_id + repeat_id

        new_post = Alarm(time=time, image=image_path,
                         repeat_id=str_id, sound_id=sound)

        db.session.add(new_post)
        db.session.commit()

        # アラーム設定
        alarm = Alarm.query.order_by(Alarm.id.desc()).first()
        setAlarm(repeat_list=repeat_list, alarm=alarm)

        return redirect('/')


@app.route('/add_alarm', methods=['POST'])
def upload():
    if request.method == 'POST':
        repeats = Repeat.query.all()
        sounds = Sound.query.all()

        upload_folder = "./uploads/"
        image = request.files['image']
        image_path = upload_folder + image.filename
        image.save(image_path)
        # ランダムなファイル名を生成
        new_filename = ''.join(random.choice(
            string.ascii_lowercase) for i in range(16))

        # ファイル名を変更したパスを生成
        ext = ".jpg"
        new_image_path = upload_folder + new_filename + ext

        # 名前変更
        image.filename = os.rename(image_path, new_image_path)

        # # HTMLから画像を表示できるようにパスの変更
        # new_image_path = "." + new_image_path

        # 画像解析処理
        # code...
        # もし画像解析が成功したらadd_alarm.htmlへ移動

        return render_template('add_alarm.html', image_path=new_image_path, repeats=repeats, sounds=sounds)


@app.route('/edit_alarm/<int:id>', methods=['GET', 'POST'])
def update(id):
    alarm = Alarm.query.get(id)
    repeats = Repeat.query.all()
    sounds = Sound.query.all()
    repeat_list = [int(x) for x in list(str(alarm.repeat_id))]

    # 編集ボタンからページにアクセスする場合
    if request.method == 'GET':
        # 編集ページの表示
        # repeat_list = [int(x) for x in list(str(alarm.repeat_id))]
        return render_template('edit_alarm.html', alarm=alarm, repeats=repeats, repeat_list=repeat_list, sounds=sounds)
    # 編集ページからアラームを編集して保存する場合
    else:
        removeAlarm(repeat_list=repeat_list, alarm=alarm)

        repeat_list = request.form.getlist('repeat')

        # 繰り返しの保存
        str_id = ""
        for repeat_id in repeat_list:
            str_id = str_id + repeat_id

        # DBに反映
        alarm.time = request.form.get('time')
        # alarm.image = request.files['image']
        alarm.repeat_id = str_id
        alarm.sound_id = request.form.get('sound')

        setAlarm(repeat_list=repeat_list, alarm=alarm)

        db.session.commit()

        # トップページに飛ばす
        return redirect('/')


@app.route('/delete_alarm/<int:id>')
def delete(id):
    alarm = Alarm.query.get(id)
    repeat_list = [int(x) for x in list(str(alarm.repeat_id))]
    dir_path = './uploads/'
    file_name = os.path.basename(alarm.image)

    # アラームに設定されてた画像を削除
    os.remove(dir_path + file_name)

    removeAlarm(repeat_list=repeat_list, alarm=alarm)

    db.session.delete(alarm)
    db.session.commit()
    return redirect('/')


@app.route('/change_flag', methods=['POST'])
def change_flag():
    alarm = Alarm.query.get(request.form['id'])
    repeat_list = [int(x) for x in list(str(alarm.repeat_id))]

    if request.form['flag'] == 'True':
        alarm.flag = False
        # アラーム停止
        pauseAlarm(repeat_list=repeat_list, alarm=alarm)
    else:
        alarm.flag = True
        # アラーム再開
        resumeAlarm(repeat_list=repeat_list, alarm=alarm)

    db.session.commit()

    return redirect('/')


@app.route('/stop_alarm', methods=['GET', 'POST'])
def photo():
    if request.method == 'GET':
        return render_template('stop_alarm.html')
    else:
        image = request.form.get('image')

        # result = imgRecognition()
        result = True

        if result == True:
            # requests.post(
            #     'https://maker.ifttt.com/trigger/stop_alarm/with/key/ehsWG5yTpSDi6wmh7X20wWEiEWk4FoMLocB2hc1eLOh')
            stopAlarm()

            return redirect('/')
        else:
            return redirect('/stop_alarm')


@app.route('/initial_data')
# データ初期化用
def initial():
    db.session.add(Repeat(repeat_name='毎月曜日'))
    db.session.add(Repeat(repeat_name='毎火曜日'))
    db.session.add(Repeat(repeat_name='毎水曜日'))
    db.session.add(Repeat(repeat_name='毎木曜日'))
    db.session.add(Repeat(repeat_name='毎金曜日'))
    db.session.add(Repeat(repeat_name='毎土曜日'))
    db.session.add(Repeat(repeat_name='毎日曜日'))

    db.session.add(Sound(sound_name='田舎のカエル'))
    db.session.add(Sound(sound_name='サイレン'))
    db.session.add(Sound(sound_name='にわとり'))
    db.session.add(Sound(sound_name='ホトトギス'))
    db.session.add(Sound(sound_name='アブラゼミ'))
    db.session.add(Sound(sound_name='Youtuberがよく流すやつ'))
    db.session.add(Sound(sound_name='チャイム'))
    db.session.add(Sound(sound_name='ドラムロール'))

    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
