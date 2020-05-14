import json
import data

goals = data.goals
goals["coding"] = "для программирования"
goalstyle = {"travel": "alert-danger", "study": "alert-success", "work": "alert-info",
              "relocate": "alert-warning", "coding": "alert-dark" }
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

jdump = {"goals": goals, "goalstyle": goalstyle, "days": days, "timesheets": timesheets, "teachers": teachers}

with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(jdump, f, ensure_ascii=False)
