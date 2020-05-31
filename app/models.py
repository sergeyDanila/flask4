import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import db

days_table = db.Table("days",
                      db.Column("id", db.Integer, primary_key=True),
                      db.Column("day", db.String(5)),
                      db.Column("day_desc", db.String(15)))


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    style = db.Column(db.String(50))
    icon = db.Column(db.String(50))


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(1500))
    rating = db.Column(db.Numeric(6, 2))
    picture = db.Column(db.String(250))
    price = db.Column(db.Numeric(12, 2))
    #   goals = db.relationship("Goal")
    booking = db.relationship("Booking", back_populates="teacher")


teach_goals = db.Table("teach_goals",
                       db.Column("teach_id", db.Integer, db.ForeignKey("teachers.id")),
                       db.Column("goal_id", db.Integer, db.ForeignKey("goals.id")))
teach_timesheet = db.Table("timesheets",
                           db.Column("teach_id", db.Integer, db.ForeignKey("teachers.id")),
                           db.Column("timesheet", db.String(250)))


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, default=datetime.now)
    remote_addr = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    day = db.Column(db.String(5))
    time = db.Column(db.String(10))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher", back_populates="booking")


timechoice = db.Table("request_timechoice",
                      db.Column("id", db.Integer, primary_key=True),
                      db.Column("day_desc", db.String(50)))


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, default=datetime.now)
    remote_addr = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    timeshoice_id = db.Column(db.Integer, db.ForeignKey("request_timechoice.id"))
    goals = db.relationship("Goal")


db.create_all()

# db.session.commit()
