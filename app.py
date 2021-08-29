import os, datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remi.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    image = db.Column(db.String(128), nullable=False)
    repeat_id = db.Column(db.Integer, default=0)
    flag = db.Column(db.Boolean, nullable=False, default=1)
    sound_id = db.Column(db.Integer, default=1)

# ホーム画面
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    else:
        time = request.form.get('time')
        image = request.files['image']
        repeat = request.form.get('repeat')
        sound = request.form.get('sound')
        
        # time = datetime.datetime(time, '%H:%M')
        # 写真のアップロード先を指定
        upload_folder = "./uploads/"
        image_path = upload_folder + image.filename
        
        # imageをアップロード
        image.save(image_path)
        
        new_post = Post(time=time, image=image_path, repeat_id=repeat, sound_id=sound)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect('/')

@app.route('/add_alarm')
def add_alarm():
    return render_template('add_alarm.html')

# 写真アップロードだけ別画面でする時用
# @app.route("/upload/",methods=["POST"])
# def upload():
#     if ("file" in request.files): #存在確認
#         upload_folder = "./uploads/"
#         file = request.files["file"]
#         file.save(os.path.join(upload_folder ,file.filename)) #file.filenameでファイル名取得
#         return redirect("/file/"+file.filename)
#     else: return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)