import os
import os.path
import random
import string
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload

app = Flask(__name__, static_folder='./uploads/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remi.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    image = db.Column(db.String(128), nullable=False)
    repeat_id = db.Column(db.Integer, default=0)
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
        posts = Post.query.all()
        repeats = Repeat.query.all()
        return render_template('index.html', posts=posts, repeats=repeats)
    else:
        time = request.form.get('time')
        image = request.files['image']
        repeat_list = request.form.getlist('repeat')
        sound = request.form.get('sound')

        # 写真のアップロード先を指定
        upload_dir = "./uploads/"
        image_path = upload_dir + image.filename
        # 写真をアップロード
        image.save(image_path)

        # ランダムなファイル名を生成
        new_filename = ''.join(random.choice(
            string.ascii_lowercase) for i in range(16))

        # ファイル名を変更したパスを生成
        ext = ".jpg"
        new_image_path = upload_dir + new_filename + ext

        # 名前変更
        image.filename = os.rename(image_path, new_image_path)

        # HTMLから画像を表示できるようにパスの変更
        new_image_path = "." + new_image_path

        # 繰り返しの保存
        str_id = ""

        for repeat_id in repeat_list:
            str_id = str_id + repeat_id

        new_post = Post(time=time, image=new_image_path,
                        repeat_id=str_id, sound_id=sound)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/')


@app.route('/add_alarm')
def create():
    # repeats = Repeat.query.all()
    # sounds = Sound.query.all()
    return render_template('add_alarm.html')


@app.route('/detail_alarm/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('edit_alarm.html', post=post)


@app.route('/edit_alarm/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    repeats = Repeat.query.all()
    sounds = Sound.query.all()

    # 編集ボタンからページにアクセスする場合
    if request.method == 'GET':
        # 編集ページの表示
        repeat_list = [int(x) for x in list(str(post.repeat_id))]
        return render_template('edit_alarm.html', post=post, repeats=repeats, repeat_list=repeat_list, sounds=sounds)
    # 編集ページからアラームを編集して保存する場合
    else:
        repeat_list = request.form.getlist('repeat')

        # 繰り返しの保存
        str_id = ""
        for repeat_id in repeat_list:
            str_id = str_id + repeat_id

        # DBに反映
        post.time = request.form.get('time')
        # post.image = request.files['image']
        post.repeat_id = str_id
        post.sound_id = request.form.get('sound')

        db.session.commit()

        # トップページに飛ばす
        return redirect('/')


@app.route('/delete_alarm/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# 写真アップロードだけ別画面でする時用
# @app.route("/upload/",methods=["POST"])
# def upload():
#     if ("file" in request.files): #存在確認
#         upload_folder = "./uploads/"
#         file = request.files["file"]
#         file.save(os.path.join(upload_folder ,file.filename)) #file.filenameでファイル名取得
#         return redirect("/file/"+file.filename)
#     else: return redirect("/")


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

    db.session.add(Sound(sound_name='レーダー'))
    db.session.add(Sound(sound_name='アップリフト'))
    db.session.add(Sound(sound_name='オープニング'))
    db.session.add(Sound(sound_name='きらめき'))
    db.session.add(Sound(sound_name='サーキット'))
    db.session.add(Sound(sound_name='さざ波'))

    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
