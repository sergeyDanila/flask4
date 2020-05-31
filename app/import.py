# грузим данные в СУБД после её создания
# вместо DELETE для очистки таблиц лучше  использовать TRUNCATE, но sqlite его не признает
import json
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import db
from app.models import Booking, Goal, Teacher, Request

with open("data.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

with open("data.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())

# Импорт целей
db.session.execute(text("DELETE FROM goals;"))
goals = []
g = []
ind = 0
for i, val in data["goals"].items():
    goals.append(Goal(id=ind, name=i, desc=val, style=data["goalstyle"][i], icon=data["goalicon"][i]))
    g.append(i)
    db.session.add(goals[ind])
    ind += 1

# Импорт справочника Дни
i = 1
s = "INSERT INTO days(id, day, day_desc)\n VALUES"
for d, desc in data["days"].items():
    s += f"({i}, '{d}', '{desc}'),\n"
    i += 1
db.session.execute(text("DELETE FROM days;"))
db.session.execute(text(s[0:-2] + ";"))

# Импорт справочника "варианты занятости"
db.session.execute(text("DELETE FROM request_timechoice;"))
db.session.execute("""INSERT INTO request_timechoice(id, day_desc)
                        VALUES    (1, "1-2 часа в неделю"),
                                  (3, "3-5 часов в неделю"),
                                  (5, "5-7 часов в неделю"),
                                (7, "7-10 часов в неделю"),
                                  (8, "Всегда готов!"); """)

# Импорт учителей
db.session.execute(text("DELETE FROM teachers;"))
db.session.execute(text("DELETE FROM teach_goals;"))
ind = 0
teachers = []

for t in data["teachers"]:
    teachers.append(Teacher(id=t["id"], name=t["name"], about=t["about"],
                            rating=t["rating"], picture=t["picture"], price=t["price"]))
    db.session.add(teachers[ind])

    s = "INSERT INTO teach_goals(teach_id, goal_id)\n VALUES"
    for i in t["goals"]:
        s += f"({t['id']}, '{g.index(i)}'),\n"

    db.session.execute(text(s[0:-2] + ";"))

    ind += 1

# Импорт расписания
i = 1
s = "INSERT INTO timesheets(teach_id, timesheet)\n VALUES"
for t in data["timesheets"]:
    s += f"({t[0]},  '{','.join(map(str, t[1]))}'),\n"
    i += 1
db.session.execute(text("DELETE FROM timesheets;"))
db.session.execute(text(s[0:-2] + ";"))

db.session.commit()
