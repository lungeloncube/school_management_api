from flask_restx import Namespace, Resource, fields

course_namespace = Namespace('course', description="Namespace for courses.py")

course_namespace.model(
    'Course', {
        'id': fields.Integer(description="course id"),
        'name': fields.String(description="course name", required=True),
        'status': fields.String(description="completion status", required=True, enum=['INPROGRESS',
                                                                                      'COMPLETE',
                                                                                      'PASSED',
                                                                                      'FAILED']),
        'mark': fields.Decimal()
    }
)


@course_namespace.route('/course')
class CourseGetCreate(Resource):
    def get(self):
        """ Get all courses.py"""
        pass

    def post(self):
        """create course"""
        pass


@course_namespace.route('/course/<int:course_id>')
class UpdateCourse(Resource):
    def patch(self, course_id):
        """update course """
        pass


@course_namespace.route('/course/<int:course_id>')
class DeleteCourse(Resource):
    def patch(self, course_id):
        """delete course """
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
