from datetime import datetime

from flask import render_template, request, redirect, url_for
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField
from wtforms.validators import InputRequired

from app import app, db
from app.models import Booking, Goal, Teacher, Request


# Цели нужны практически во всех роутах залезем за ними в базу всего 1 раз
res = db.session.query(Goal)
goals = dict()
goalstyle = dict()
goalicon = dict()
for g in res.all():
    goals[g.name] = g.desc
    goalstyle[g.name] = g.style
    goalicon[g.name] = g.icon

# Справочник дней
days = dict(db.session.execute(text("select day, day_desc from days order by id")).fetchall())


class RequestForm(FlaskForm):
    goals = RadioField('Какая цель занятий?', choices=goals.items(), default='travel')
    hours = RadioField(label='Сколько времени есть?',
                       choices=[(r.id, r.day_desc) for r in
                                db.session.execute(text("SELECT id, day_desc FROM request_timechoice;"))], default=3)
    name = StringField('Имя', [InputRequired(message="Введите имя")])
    phone = StringField('Контакты', [InputRequired(message="Введите контактную информацию")])


class BookingForm(FlaskForm):
    teacher = HiddenField()
    day = HiddenField()
    time = HiddenField()
    name = StringField('Вас зовут', [InputRequired(message="Введите имя")])
    phone = StringField('Контактная информация', [InputRequired(message="Введите контактную информацию")])


@app.template_filter('band')  # Фильтр побитовое И
def band(a, b):
    return int(a) & int(b)


@app.route('/')  # / – здесь будет главная
def render_index():
    teachers = db.session.query(Teacher).order_by(db.func.random()).limit(6)

    return render_template('index.html',
                           teachers=teachers,
                           goals=goals,
                           goalstyle=goalstyle,
                           goalicon=goalicon,
                           )


@app.route('/all/')  # / – здесь будут все предподаватели
def render_all():
    teachers = db.session.query(Teacher)

    return render_template('index.html',
                           teachers=teachers,
                           goals=goals,
                           goalstyle=goalstyle,
                           goalicon=goalicon,
                           )


@app.route('/goals/<goal>/')  # - цели /goals/<goal>/  – здесь будет цель
def render_goals(goal):
    # teachers = [t for t in data["teachers"] if (t["goals"]).count(goal) == 1]
    sql = f"""select t.id, t.name, t.about,t.rating, t.picture, t.price 
              from teachers t join teach_goals tg on t.id=tg.teach_id join goals g on tg.goal_id=g.id 
              where g.name='{goal}';"""
    teachers = db.session.execute(text(sql))
    gl = db.session.query(Goal).filter(Goal.name == goal).first()
    return render_template('goal.html',
                           teachers=teachers,
                           goalstyle=gl.style,
                           goalicon=gl.icon,
                           goaldesc=gl.desc,
                           goal=goal)


@app.route('/profiles/<int:teacherid>/')  # /profiles/<id учителя>/ – здесь будет преподаватель
def render_profile(teacherid):
    # teacher = [t for t in data["teachers"] if t["id"] == teacherid][0]
    t = db.session.query(Teacher).get_or_404(teacherid)
    teacher = t

    sql = f"select timesheet from timesheets where teach_id={teacherid}"
    timesheet = db.session.execute(text(sql)).first()


    sql = f"select name,desc,style,icon from goals g join teach_goals t on g.id = t.goal_id where teach_id = {teacherid}"
    tg = db.session.execute(text(sql)).fetchall()
    teachgoals = []
    goalsdesc = []
    goalstyle = []
    goalsicon = []

    for i in tg:
        teachgoals.append(i.name)
        goalsdesc.append(i.desc)
        goalstyle.append(i.style)
        goalsicon.append(i.icon)

    return render_template('profile.html',
                           teacherid=teacherid,
                           teacher=teacher,
                           teachgoals=teachgoals,
                           goalsdesc=goalsdesc,
                           goalstyle=goalstyle,
                           goalsicon=goalsicon,
                           timesheet=list(map(int, timesheet[0].split(','))),
                           days=days)


@app.route('/request/',
           methods=['GET', 'POST'])  # /request_done/ – заявка на подбор отправлена
def render_request():
    form = RequestForm()
    if request.method == 'POST':
        name = form.name.data
        phone = form.phone.data
        goal = form.goals.data
        glabel = db.session.query(Goal).filter(Goal.name == goal).first()
        hour = form.hours.data
        sql = f"SELECT day_desc FROM request_timechoice where id = {hour};"
        hlabel = db.session.execute(text(sql)).first()
        created = datetime.now()
        db.session.add(Request(created=created,
                               remote_addr=request.remote_addr,
                               name=name,
                               phone=phone,
                               goal_id=glabel.id,
                               timeshoice_id=hour))
        db.session.commit()

        return render_template('request_done.html',
                               name=name,
                               phone=phone,
                               goal=glabel.desc,
                               hour=hlabel[0])
    return render_template('request.html', form=form)



@app.route('/booking/<int:teacherid>/<day>/<time>/',
           methods=["GET", "POST"])  # формы бронирования <id учителя>/<день недели>/<время>/
def render_booking(teacherid, day, time):
    form = BookingForm(teacher=teacherid, day=day, time=time)
    if request.method == 'POST':
        name = form.name.data
        phone = form.phone.data
        teacher = form.teacher.data
        day = form.day.data
        time = form.time.data
        db.session.add(Booking(created=datetime.now(),
                               remote_addr=request.remote_addr,
                               name=name,
                               phone=phone,
                               day=day,
                               time=time,
                               teacher_id=teacherid))
        db.session.commit()

        return render_template('booking_done.html',
                               name=name,
                               phone=phone,
                               teacher=teacher,
                               time=time,
                               day=days[day])
    
    return render_template('booking.html',
                           teacherid=teacherid,
                           teacher=db.session.query(Teacher).get_or_404(teacherid),
                           daydesc=days[day],
                           day=day,
                           time=time,
                           form=form)

