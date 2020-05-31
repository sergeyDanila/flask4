# первоначальная загрузка data.py->data.json
import json
import app.data as data

goals = data.goals
goals["coding"] = "Для программирования"
goalstyle = {"travel": "danger", "study": "success", "work": "info",
             "relocate": "secondary", "coding": "dark"}
goalicon = {"travel": "fas fa-map-marked-alt", "study": "fas fa-user-graduate", "work": "fas fa-business-time",
            "relocate": "fas fa-tractor", "coding": "fas  fa-laptop-code"}
days = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг",
        "fri": "Пятница", "sat": "Суббота", "sun": "Воскресенье"}
teachers = []
timesheets = []
for teach in data.teachers:
    timesheet = []
    for day, time in teach["free"].items():
        timesheet.append(int(time['8:00']) +
                         int(time['10:00']) * 2 +
                         int(time['12:00']) * 4 +
                         int(time['14:00']) * 8 +
                         int(time['16:00']) * 16 +
                         int(time['18:00']) * 32 +
                         int(time['20:00']) * 64 +
                         int(time['22:00']) * 128
                         )
    timesheets.append([teach["id"], timesheet])
    del teach["free"]
    teachers.append(teach)
    if 8 <= teach["id"] <= 11:
        teach["goals"].append("coding")

jdump = {"goals": goals, "goalstyle": goalstyle, "goalicon": goalicon, "days": days, "timesheets": timesheets,
         "teachers": teachers}

with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(jdump, f, ensure_ascii=False)
