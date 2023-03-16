from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
from http import HTTPStatus
from flask_jwt_extended import jwt_required


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


@course_namespace.route('/course/<int:course_id>')
class GetUpdateDeleteCourse(Resource):
    @course_namespace.marshal_with(course_model)
    def get(self, course_id):
        """get course by id """
        course=Course.get_by_id(course_id)
        return course, HTTPStatus.OK
    def patch(self, course_id):
        """update course  """
        pass
    def delete(self, course_id):
        """delete course by id """
        pass


@course_namespace.route('/course/<int:course_id>/<int:user_id>')
class RegisterUserToCourse(Resource):
    def post(self, user_id):
        """Registers user to course"""
        pass


@course_namespace.route('/course/<int:course_id>/<int:user_id>')
class DeRegisterUserFromCourse(Resource):
    def delete(self, user_id, course_id):
        """DeRegisters user from course"""
        pass
