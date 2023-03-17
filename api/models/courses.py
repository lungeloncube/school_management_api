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
    name = db.Column(db.String(), nullable=False)
    status = db.Column(db.Enum(Statuses), default=Statuses.INPROGRESS)
    # user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    courses_work = db.relationship('CourseWork', backref='courses', lazy=True)
    user = db.relationship("User", secondary="users_to_courses")

    def __repr__(self):
        return f"<Course {self.id}"


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)


    def delete(self):
        db.session.delete(self)
        db.session.commit()




