from ..utilities import db
from enum import Enum


class Statuses(Enum):
    INPROGRESS = 'inprogress'
    COMPLETE = 'complete'
    PASSED = 'passed'
    FAILED = 'failed'


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.Enum(Statuses), default=Statuses.INPROGRESS)
    mark = db.Column(db.Double(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))


    def __repr__(self):
        return f"<Course {self.id}"
