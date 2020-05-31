import json
from app import app, db
from app.jsonsave import jsonsave
from sqlalchemy import text
from app.models import Booking, Goal, Teacher, Request

goal = "travel"
sql = f"select t.id, t.name, t.about,t.rating, t.picture, t.price from teachers t join teach_goals tg on t.id=tg.teach_id join goals g on tg.goal_id=g.id where g.name='{goal}';"
teachers = dict(db.session.execute(text(sql)).fetchone())

print(teachers)

res = db.session.query(Goal)

goals = dict()
goalstyle = dict()
goalicon = dict()
for g in res.all():
    goals[g.name] = g.desc
    goalstyle[g.name] = g.style
    goalicon[g.name] = g.icon

print(goalstyle)

days = dict(db.session.execute(text("select day, day_desc from days order by id")).fetchall())
print(days)

sql = f"select timesheet from timesheets where teach_id={1}"
timesheet = db.session.execute(text(sql)).first()
#list(map(int, timesheet[0].split(',')))


glabel = db.session.query(Goal).filter(Goal.name == goal).first()

print(glabel.id)