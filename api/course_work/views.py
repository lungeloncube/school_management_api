from flask_restx import Resource, Namespace, fields

from ..models.course_work import CourseWork
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.users import User
from ..models.courses import Course

from http import HTTPStatus

course_work_namespace = Namespace('course_work', description="Namespace for course work")
course_work_model = course_work_namespace.model(
    'CourseWork', {
        'mark': fields.String(description=""),
    }
)


@course_work_namespace.route('/student/<int:user_id>/course/<int:course_id>')
class AddCourseWork(Resource):
    # @course_work_namespace.marshal_with(course_work_model)
    @jwt_required()
    def post(self, user_id, course_id):
        """ Add course work.py"""
        data = course_work_namespace.payload
        logged_user = User.query.filter_by(email=get_jwt_identity()).first()
        if logged_user.is_admin or logged_user.is_staff:
            student = User.get_by_id(user_id)
            course = Course.get_by_id(course_id)

            if student is not None:
                if course is not None:
                    # check if registered for course
                    if any(course == course for x in student.courses):
                        course_work = CourseWork(
                            mark=data['mark']
                        )
                        course_work.save()
                        student.courses_work.append(course_work)
                        student.save()
                        course.courses_work.append(course_work)
                        course.save()
                        return {"Success": "marks saved for: " + student.name}, HTTPStatus.OK
                    else:
                        return {"Failed": "student not registered for this course"},HTTPStatus.BAD_REQUEST


                else:
                    return {"Failed": "Course not found: "}, HTTPStatus.NOT_FOUND
            return {"Failed": "Student with that id is not found: "}, HTTPStatus.NOT_FOUND
        else:
            return {"Failed": "You do not have permission to do this operation"}, HTTPStatus.FORBIDDEN
