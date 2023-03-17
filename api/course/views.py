from flask_restx import Namespace, Resource, fields

from ..models.users_to_courses import UserToCourse
from ..models.courses import Course
from http import HTTPStatus
from flask_jwt_extended import jwt_required
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
        data = course_namespace.payload
        new_course = Course(
            id=data['id'],
            name=data['name'],
            status=data['status']
        )
        new_course.save()
        return new_course, HTTPStatus.CREATED


@course_namespace.route('/course/<int:user_id>/courses')
class UserCourses(Resource):
    @course_namespace.marshal_with(course_model)
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


@course_namespace.route('/course/<int:course_id>')
class GetUpdateDeleteCourse(Resource):
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self, course_id):
        """get course by id """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    def patch(self, course_id):
        """update course  """
        data = course_namespace.payload
        course = Course.get_by_id(course_id)
        if course is not None:
            course.name = data['name']
            course.status = data['status']

            course.save()
            return course, HTTPStatus.OK

    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def delete(self, course_id):
        """delete course by id """
        course = Course.get_by_id(course_id)
        if course is not None:
            course.delete()
            return course, HTTPStatus.NO_CONTENT


@course_namespace.route('/course/<int:course_id>/<int:user_id>')
class RegisterUserToCourse(Resource):
    def patch(self, user_id, course_id):
        """Registers user to course"""
        course = Course.get_by_id(course_id)
        if course is not None:
            user = User.get_by_id(user_id)
            # user.courses = [course]

            user.courses.append(course)
            user.save()
            return {"success": True}


@course_namespace.route('/course/<int:course_id>/<int:user_id>')
class DeRegisterUserFromCourse(Resource):
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    def post(self, user_id, course_id):
        """DeRegisters user from course"""
        user = User.get_by_id(user_id)
        user_courses = User.query.join(UserToCourse).join(Course).filter((UserToCourse.user_id ==
                                                                          user.id)).first()
        # user_courses.delete()

        if user_courses is not None:
            return user_courses, {"success": "Student deregistered"}
