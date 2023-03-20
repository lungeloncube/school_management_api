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
                        return {"Failed": "student not registered for this course"}, HTTPStatus.BAD_REQUEST


                else:
                    return {"Failed": "Course not found: "}, HTTPStatus.NOT_FOUND
            return {"Failed": "Student with that id is not found: "}, HTTPStatus.NOT_FOUND
        else:
            return {"Failed": "You do not have permission to do this operation"}, HTTPStatus.FORBIDDEN


@course_work_namespace.route('/student/marks/<int:student_id>')
class GetStudentMarks(Resource):

    @jwt_required()
    def get(self, student_id):
        """Get user by id"""

        user = User.get_by_id(student_id)
        logged_user = User.query.filter_by(email=get_jwt_identity()).first()
        if logged_user.email == user.email or logged_user.is_staff or logged_user.is_admin:
            cw = []

            if user is not None:
                student_courses = user.courses

                for course in student_courses:
                    cowor = user.courses_work

                    for c in cowor:
                        cw.append({"mark": c.mark, "course_name": course.name})

                return cw, HTTPStatus.OK
        else:
            return {"Failed": "You do not have permissions to view this record"}, HTTPStatus.FORBIDDEN


@course_work_namespace.route('/overall-gpa/<int:student_id>')
class GetOverallGPA(Resource):
    def get(self, student_id):

        """
        get user gpa
        """
        user = User.get_by_id(student_id)

        total_course_work = 0
        if user is not None:

            cowor = user.courses_work
            if len(cowor) > 0:

                for c in cowor:
                    total_course_work += c.mark

                average_mark = (total_course_work / (len(cowor) * 100)) * 100
                gpa = calculate_gpa(average_mark)
                return {"GPA": gpa, "average_mark": average_mark}, HTTPStatus.OK
            else:
                return {"Message": "This student has no course work"}, HTTPStatus.OK
        else:
            return {"Message": "This student has no course work"}, HTTPStatus.OK


@course_work_namespace.route('/overall-gpa/student/<int:student_id>/course/<int:course_id>')
class GetCourseGPA(Resource):
    def get(self, student_id, course_id):

        """
        get user gpa for one course
        """
        user = User.get_by_id(student_id)
        course = Course.get_by_id(course_id)

        total_course_work = 0
        if user is not None:
            if course is not None:

                cowor = user.courses_work

                for c in cowor:
                    if c.course == course.id:
                        total_course_work += c.mark

                if len(cowor) > 0:

                    average_mark = (total_course_work / (len(cowor) * 100)) * 100
                    gpa = calculate_gpa(average_mark)
                    return {"GPA": gpa, "average_mark": average_mark, "course name": course.name}, HTTPStatus.OK
                else:
                    return {
                        "failed": "no course work"
                    }

            else:
                return {
                    "failed": "no course work"
                }
        else:
            return {"Message": "This student has no course work"}, HTTPStatus.OK


def calculate_gpa(mark):
    if mark >= 70:
        gpa = 1
        return gpa
    elif 60 <= mark < 70:
        gpa = 2.1
        return gpa
    elif 54 <= mark < 60:
        gpa = 2.2
        return gpa
    elif 50 <= mark < 54:
        gpa = 3
        return gpa
    else:
        return "fail"
