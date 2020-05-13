import json
from flask import Flask, render_template

app = Flask(__name__)


with open('data.json', 'r', encoding="utf-8") as f:
    data = json.loads(f.read())

@app.route('/')  # - главной / – здесь будет главная
def render_index():
    return render_template('index.html',
                           )


@app.route('/goals/<goal>/')  # - цели /goals/<goal>/  – здесь будет цель
def render_goals(goal):
    return render_template('goal.html',
                           goal=goal)


@app.route('/profiles/<teacherid>/')  # - профиля учителя /profiles/<id учителя>/ – здесь будет преподаватель
def render_profile(teacherid):
    return render_template('profile.html',
                           teacherid=teacherid,
                           teacher=1)


@app.route('/request/')  # - заявки на подбор /request/ – здесь будет заявка на подбор
def render_request():
    return render_template('request.html',
                           )


@app.route('/request_done/ ')  # - принятой заявки на подбор /request_done/ – заявка на подбор отправлена
def render_reqdone():
    return render_template('request_done.html',
                           )


@app.route('/booking/<teacherid>/<day>/<time>')  # - формы бронирования <id учителя>/<день недели>/<время>/
def render_booking(teacherid, day, time):
    return render_template('booking.html',
                           teacherid=teacherid,
                           day=teacherid,
                           time=teacherid)


@app.route('/booking_done/ ')  # - - принятой заявки на подбор /booking_done/   – заявка отправлена.
def render_bookdone():
    return render_template('booking_done.html',
                           )


if __name__ == '__main__':
    app.run(debug=True)
