from flask_restx import Namespace, Resource, fields

from ..models.courses import Course
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.users import User

course_namespace = Namespace('course', description="Namespace for courses.py")

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description="course id"),
        'name': fields.String(description="course name", required=True),
        'status': fields.String(description="completion status", required=True, enum=['INPROGRESS',
                                                                                      'COMPLETE',
                                                                                      'PASSED',
                                                                                      'FAILED']),

    }
)


@course_namespace.route('/courses')
class CourseGetCreate(Resource):
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self):
        """ Get all courses"""
        courses = Course.query.all()
        return courses, HTTPStatus.OK

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def post(self):
        """create course"""
        logged_user = User.query.filter_by(email=get_jwt_identity()).first()

        data = course_namespace.payload
        courses=Course.query.filter_by(name=data['name']).all()
        if logged_user.is_admin or logged_user.is_staff:
            if len(courses)<0:
                new_course = Course(
                    id=data['id'],
                    name=data['name'],
                    status=data['status']
                )
                new_course.save()
                return new_course, HTTPStatus.CREATED
            else:
                return {"Failed":"Course with that name already exists"},HTTPStatus.BAD_REQUEST
        else:
            return  {"Failed":"You do not have permissions to add  a course"},HTTPStatus.FORBIDDEN



@course_namespace.route('/course/<int:user_id>/courses')
class UserCourses(Resource):
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self, user_id):
        """
        Get all specific courses.py for a user
        :param user_id:
        :return:
        """
        user = User.get_by_id(user_id)
        if user is not None:
            courses = user.courses
            return courses, HTTPStatus.OK
        else:
            return {"Failed":"User with provided iD does not exist"},HTTPStatus.BAD_REQUEST


@course_namespace.route('/course/<int:course_id>')
class GetUpdateDeleteCourse(Resource):
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self, course_id):
        """get course by id """
        course = Course.get_by_id(course_id)
        if course is not None:
            return course, HTTPStatus.OK
        else:
            return {"Failed": "course with that ID does not exist"}, HTTPStatus.NOT_FOUND

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def patch(self, course_id):
        """update course  """
        data = course_namespace.payload
        course = Course.get_by_id(course_id)
        if course is not None:
            course.name = data['name']
            course.status = data['status']

            course.save()
            return course, HTTPStatus.OK
        else:
            return {"Failed":"Course with provided id does not exist"}, HTTPStatus.BAD_REQUEST

    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def delete(self, course_id):
        """delete course by id """
        course = Course.get_by_id(course_id)
        if course is not None:
            course.delete()
            return course, HTTPStatus.NO_CONTENT
        else:
            return {"failed":"Course not found"}, HTTPStatus.BAD_REQUEST


@course_namespace.route('/course/<int:course_id>/<int:user_id>')
class RegisterUserToCourse(Resource):
    @jwt_required()
    def patch(self, user_id, course_id):
        """Registers user to course"""
        course = Course.get_by_id(course_id)
        if course is not None:
            user = User.get_by_id(user_id)
            logged_user = User.query.filter_by(email=get_jwt_identity()).first()
            if logged_user.email == user.email or logged_user.is_admin or logged_user.is_staff:
                user.courses.append(course)
                user.save()
                return {"success": "Student registered for: " + course.name}
            else:
                return {"Failed": "You can not perform this action"}, HTTPStatus.FORBIDDEN
        else:
            return {"Failed": "This course does not exist"}, HTTPStatus.BAD_REQUEST


@course_namespace.route('/course/deregister/<int:course_id>/<int:student_id>')
class DeRegisterUserFromCourse(Resource):
    @jwt_required()
    def post(self, student_id, course_id):
        """DeRegisters user from course"""
        student = User.get_by_id(student_id)
        if student is not None:
            logged_user = User.query.filter_by(email=get_jwt_identity()).first()
            if logged_user.is_admin or logged_user.email == student.email:

                course = Course.get_by_id(course_id)
                student.courses.remove(course)
                student.save()
                return {"success": " deregistered from: " + course.name}
            else:
                return {"Failed": " You do not have permission to carry out this operation, contact admin"}
        else:
            return {"Failed": " Student with this id does not exist"}
