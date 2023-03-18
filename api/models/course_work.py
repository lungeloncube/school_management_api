from ..utilities import db


class CourseWork(db.Model):
    __tablename__ = 'course_work'
    id = db.Column(db.Integer(), primary_key=True)
    mark = db.Column(db.Double(), nullable=False)
    course = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))


    def __repr__(self):
        return f"<CourseWork {self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()
