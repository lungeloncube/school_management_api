from sqlalchemy.orm import relationship, backref
from ..utilities import db


class UserToCourse(db.Model):
    __tablename__ = 'users_to_courses'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))

    # ... any other fields

    user = relationship('User', backref=backref("users_to_courses", cascade="all, delete-orphan"))
    course = relationship('Course', backref=backref("users_to_courses", cascade="all, delete-orphan"))
