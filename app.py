import json
from random import shuffle
from flask import Flask, render_template

import filter

app = Flask(__name__)


with open('data.json', 'r', encoding="utf-8") as f:
    data = json.loads(f.read())


@app.template_filter('band')  # Фильтр побитовое И
def band(a, b):
    return int(a) & int(b)


@app.route('/')  # - главной / – здесь будет главная
def render_index():
    teachers = data["teachers"]
    shuffle(teachers)
    return render_template('index.html',
                           teachers=teachers[:6],
                           goals=data["goals"],
                           goalstyle=data["goalstyle"],
                           goalicon=data["goalicon"],
                           )


@app.route('/goals/<goal>/')  # - цели /goals/<goal>/  – здесь будет цель
def render_goals(goal):
    teachers = [t for t in data["teachers"] if (t["goals"]).count(goal) == 1]
    return render_template('goal.html',
                           teachers=teachers,
                           goalstyle=data["goalstyle"].get(goal),
                           goalicon=data["goalicon"].get(goal),
                           goaldesc=data["goals"].get(goal),
                           goal=goal)


@app.route('/profiles/<int:teacherid>/')  # - профиля учителя /profiles/<id учителя>/ – здесь будет преподаватель
def render_profile(teacherid):
    teacher = [t for t in data["teachers"] if t["id"] == teacherid][0]
    teachgoals = teacher["goals"]
    timesheet = [t for t in data["timesheets"] if t[0] == teacherid][0][1]
    days = data["days"]
    goalsdesc = []
    goalstyle = []
    goalsicon = []
    for i in teachgoals:
        goalsdesc.append(data["goals"][i])
        goalstyle.append(data["goalstyle"][i])
        goalsicon.append(data["goalicon"][i])

    return render_template('profile.html',
                           teacherid=teacherid,
                           teacher=teacher,
                           teachgoals=teachgoals,
                           goalsdesc=goalsdesc,
                           goalstyle=goalstyle,
                           goalsicon=goalsicon,
                           timesheet=timesheet,
                           days=days)


@app.route('/request/')  # - заявки на подбор /request/ – здесь будет заявка на подбор
def render_request():
    return render_template('request.html',
                            goals=data["goals"],
                           )


@app.route('/request_done/ ')  # - принятой заявки на подбор /request_done/ – заявка на подбор отправлена
def render_reqdone():
    return render_template('request_done.html',
                           )


@app.route('/booking/<int:teacherid>/<day>/<time>/')  # - формы бронирования <id учителя>/<день недели>/<время>/
def render_booking(teacherid, day, time):
    return render_template('booking.html',
                           teacherid=teacherid,
                           teacher=[t for t in data["teachers"] if t["id"] == teacherid][0],
                           daydesc=data["days"].get(day),
                           time=time)


@app.route('/booking_done/ ')  # - - принятой заявки на подбор /booking_done/   – заявка отправлена.
def render_bookdone():
    return render_template('booking_done.html',
                           )


if __name__ == '__main__':
    app.run(debug=True)
