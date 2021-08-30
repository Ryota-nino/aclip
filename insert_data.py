from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///remi.db'
db = SQLAlchemy(app)


class Repeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repeat_name = db.Column(db.String, nullable=False)


repeats = Repeat.query.all()

db.session.add(Repeat(repeat_name='毎月曜日'))
db.session.add(Repeat(repeat_name='毎火曜日'))
db.session.add(Repeat(repeat_name='毎水曜日'))
db.session.add(Repeat(repeat_name='毎木曜日'))
db.session.add(Repeat(repeat_name='毎金曜日'))
db.session.add(Repeat(repeat_name='毎土曜日'))
db.session.add(Repeat(repeat_name='毎日曜日'))
db.session.commit()
