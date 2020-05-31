from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    style = db.Column(db.String,)
    icon = db.Column(db.String)


db.create_all()

user = User(name='Василий')
db.session.add(user)
db.session.commit()


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    kitchen = db.Column(db.String)
    rates = db.relationship('Rate', back_populates='restaurant')

    def get_rating(self, uid):
        return db.session.execute('SELECT avg(rates) FROM rates where restaurant_id=:u', {'u': uid})


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    rates = db.relationship('Rate', back_populates='user')


class Rate(db.Model):
    __tablename__ = 'rates'
    uid = db.Column(db.Integer, primary_key=True)
    rates = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.uid'))
    user = db.relationship('User', back_populates='rates')
    restaurant = db.relationship('Restaurant', back_populates='rates')


db.create_all()

s = input()
rest = []
for i in range(3):
    r = input().split(', ')
    rest.append(Restaurant(uid=r[0], name=r[1], kitchen=r[2]))
    db.session.add(rest[i])

s = input()
u = []
for i in range(3):
    r = input().split(', ')
    u.append(User(uid=r[0], name=r[1]))
    db.session.add(u[i])
    db.session.query(Users).filter(Users.Name).between()

s = input()
rt = []
for i in range(9):
    r = input().split(', ')
    rt.append(Rate(restaurant_id=r[0], user_id=r[1], rates=r[2]))
    db.session.add(rt[i])

db.session.commit()

rst = db.session.query(Restaurant).all()
rating = db.session.query(Rate).all()

for r in rst:
    print(r.name, r.get_rating(r.uid))

