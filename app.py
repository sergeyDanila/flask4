from datetime import datetime
import json
from random import shuffle

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField
from wtforms.validators import InputRequired

from jsonsave import jsonsave

app = Flask(__name__)
app.secret_key = "YOHOHO & Rum bottle!"

with open('data.json', 'r', encoding="utf-8") as f:
    data = json.loads(f.read())

choice = [('1', '1-2 часа в неделю'),
          ('3', '3-5 часов в неделю'),
          ('5', '5-7 часов в неделю'),
          ('7', '7-10 часов в неделю'),
          ('8', 'Всегда готов!')]


class RequestForm(FlaskForm):
    goals = RadioField('Какая цель занятий?', choices=data["goals"].items())
    hours = RadioField('Сколько времени есть?', choices=choice)
    name = StringField('Имя')
    phone = StringField('Контакты', [InputRequired(message="Введите контактную информацию")])


class BookingForm(FlaskForm):
    teacher = HiddenField()
    day = HiddenField()
    time = HiddenField()
    name = StringField('Вас зовут')
    phone = StringField('Контактная информация', [InputRequired(message="Введите контактную информацию")])


@app.template_filter('band')  # Фильтр побитовое И
def band(a, b):
    return int(a) & int(b)


@app.route('/')  # / – здесь будет главная
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


@app.route('/profiles/<int:teacherid>/')  # /profiles/<id учителя>/ – здесь будет преподаватель
def render_profile(teacherid):
    teacher = [t for t in data["teachers"] if t["id"] == teacherid][0]
    timesheet = [t for t in data["timesheets"] if t[0] == teacherid][0][1]
    days = data["days"]
    goalsdesc = []
    goalstyle = []
    goalsicon = []

    teachgoals = teacher["goals"]
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


@app.route('/request/')  # /request/ – здесь будет заявка на подбор
def render_request():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/',
           methods=['GET', 'POST'])  # /request_done/ – заявка на подбор отправлена
def render_reqdone():
    form = RequestForm()
    if request.method == 'POST':
        name = form.name.data
        phone = form.phone.data
        goal = form.goals.data
        glabel = data["goals"].get(goal)
        hour = form.hours.data
        hlabel = [val for key, val in choice if key == hour][0]

        save = {"timestamp": str(datetime.now())}
        save["request"] = [name, phone, goal, glabel, hour, hlabel]
        jsonsave('request.json', save)

        return render_template('request_done.html',
                               name=name,
                               phone=phone,
                               goal=glabel,
                               hour=hlabel)
    return render_template('request.html', form=form)


@app.route('/booking/<int:teacherid>/<day>/<time>/',
           methods=["GET", "POST"])  # формы бронирования <id учителя>/<день недели>/<время>/
def render_booking(teacherid, day, time):
    form = BookingForm(teacher=teacherid, day=day, time=time)
    return render_template('booking.html',
                           teacherid=teacherid,
                           teacher=[t for t in data["teachers"] if t["id"] == teacherid][0],
                           daydesc=data["days"].get(day),
                           time=time,
                           form=form)


@app.route('/booking_done/',
           methods=['GET', 'POST'])  # принятой формы бронирования /booking_done/   – заявка отправлена.
def render_bookdone():
    form = BookingForm()
    if request.method == 'POST':
        name = form.name.data
        phone = form.phone.data
        teacher = form.teacher.data
        day = form.day.data
        time = form.time.data

        save = {"timestamp": str(datetime.now()), "booking": [name, phone, teacher, day, time]}
        jsonsave('booking.json', save)

        return render_template('booking_done.html',
                               name=name,
                               phone=phone,
                               teacher=teacher,
                               time=time,
                               day=data["days"].get(day))
    return render_template("booking.html", form=form)


if __name__ == '__main__':
    app.run()