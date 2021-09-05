import os
import os.path
import random
import string
from typing import SupportsRound
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload
import schedule
import time

app = Flask(__name__, static_folder='./uploads/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remi.db'
db = SQLAlchemy(app)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        alarms = Alarm.query.all()
        repeats = Repeat.query.all()

        week_list = {"1": "月", "2": "火", "3": "水",
                     "4": "木", "5": "金", "6": "土", "7": "日"}

        with open('test.py', 'w') as f:
            f.write('from alarm import Alarm\n')
            f.write('import schedule\n')
            f.write('import time\n')
            f.write('\n')
            f.write('def startAlarm():\n')
            f.write('    print("時間です")\n')
            f.write('    Sound()\n')
            f.write('\n')
            f.write('def Sound():\n')
            f.write('    print("音楽再生")\n')
            f.write('\n')
            alarms = Alarm.query.all()

            print(alarms)

            for alarm in alarms:
                repeat_list = [int(x) for x in list(str(alarm.repeat_id))]

                for repeat_id in repeat_list:
                    print(repeat_id)
                    if repeat_id == 1:
                        set_alarm = 'schedule.every().monday.at("%s").do(Alarm)\n' % (alarm.time)
                    elif repeat_id == 2:
                        set_alarm = 'schedule.every().tuesday.at("%s").do(Alarm)\n' % (alarm.time)
                    elif repeat_id == 3:
                        set_alarm = 'schedule.every().wednesday.at("%s").do(Alarm)\n' % (alarm.time)
                    elif repeat_id == 4:
                        set_alarm = 'schedule.every().thursday.at("%s").do(Alarm)\n' % (alarm.time)
                    elif repeat_id == 5:
                        set_alarm = 'schedule.every().friday.at("%s").do(Alarm)\n' % (alarm.time)
                    elif repeat_id == 6:
                        set_alarm = 'schedule.every().saturday.at("%s").do(Alarm)\n' % (alarm.time)
                    elif repeat_id == 7:
                        set_alarm = 'schedule.every().sunday.at("%s").do(Alarm)\n' % (alarm.time)

                    f.write(set_alarm)

            f.write('\n')
            f.write('while True:\n')
            f.write('    schedule.run_pending()\n')
            f.write('    time.sleep(1)\n')

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

        # アラーム設定
        schedule.every().day.at(time).do(Alarm)

        db.session.add(new_post)
        db.session.commit()

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


# @app.route('/add_alarm')
# def create():
#     repeats = Repeat.query.all()
#     sounds = Sound.query.all()
#     return render_template('add_alarm.html', repeats=repeats, sounds=sounds)


# @app.route('/detail_alarm/<int:id>')
# def read(id):
#     alarm = Alarm.query.get(id)
#     return render_template('edit_alarm.html', alarm=alarm)


@app.route('/edit_alarm/<int:id>', methods=['GET', 'POST'])
def update(id):
    alarm = Alarm.query.get(id)
    repeats = Repeat.query.all()
    sounds = Sound.query.all()

    # 編集ボタンからページにアクセスする場合
    if request.method == 'GET':
        # 編集ページの表示
        repeat_list = [int(x) for x in list(str(alarm.repeat_id))]
        return render_template('edit_alarm.html', alarm=alarm, repeats=repeats, repeat_list=repeat_list, sounds=sounds)
    # 編集ページからアラームを編集して保存する場合
    else:
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

        db.session.commit()

        # トップページに飛ばす
        return redirect('/')


@app.route('/delete_alarm/<int:id>')
def delete(id):
    alarm = Alarm.query.get(id)
    dir_path = './uploads/'
    file_name = os.path.basename(alarm.image)

    # アラームに設定されてた画像を削除
    os.remove(dir_path + file_name)

    db.session.delete(alarm)
    db.session.commit()
    return redirect('/')


@app.route('/change_flag', methods=['POST'])
def change_flag():
    alarm = Alarm.query.get(request.form['id'])

    app.logger.debug(alarm.flag)

    if request.form['flag'] == 'True':
        alarm.flag = False
    else:
        alarm.flag = True

    # app.logger.debug(alarm.flag)
    # app.logger.debug(not 0)

    db.session.commit()

    return redirect('/')


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


def set_alarm():
    with open('test.py', 'w') as f:
        f.write('from alarm import Alarm\n')
        f.write('import schedule\n')
        f.write('import time\n')
        f.write('import set_alarm\n')
        f.write('\n')
        f.write('def startAlarm():\n')
        f.write('    print("時間です")\n')
        f.write('    Sound()\n')
        f.write('\n')
        f.write('def Sound():\n')
        f.write('    print("音楽再生")\n')
        f.write('\n')
        alarms = Alarm.query.all()

        for alarm in alarms:
            repeat_list = [int(x) for x in list(str(alarm.repeat_id))]
            for repeat_id in repeat_list:
                if repeat_id == "1":
                    f.write(
                        'schedule.every().monday.at(${alarm.time}).do(Alarm)\n')
                elif repeat_id == "2":
                    f.write(
                        'schedule.every().tuesday.at(${alarm.time}).do(Alarm)\n')
                elif repeat_id == "3":
                    f.write(
                        'schedule.every().wednesday.at(${alarm.time}).do(Alarm)\n')
                elif repeat_id == "4":
                    f.write(
                        'schedule.every().thursday.at(${alarm.time}).do(Alarm)\n')
                elif repeat_id == "5":
                    f.write(
                        'schedule.every().friday.at(${alarm.time}).do(Alarm)\n')
                elif repeat_id == "6":
                    f.write(
                        'schedule.every().saturday.at(${alarm.time}).do(Alarm)\n')
                elif repeat_id == "7":
                    f.write(
                        'schedule.every().sunday.at(${alarm.time}).do(Alarm)\n')

        f.write('\n')
        f.write('while True:\n')
        f.write('    schedule.run_pending()\n')
        f.write('    time.sleep(1)\n')


if __name__ == '__main__':
    app.run(debug=True)
