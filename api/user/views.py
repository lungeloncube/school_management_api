from flask_restx import Resource, Namespace

user_namespace = Namespace('user', description="Namespace for user")


@user_namespace.route('/user')
class UserGetCreate(Resource):
    def get(self):
        """ Get all users.py"""
        pass

    def post(self):
        """create users.py"""
        pass


@user_namespace.route('/user/<int:user_id>')
class GetUpdateDelete(Resource):
    def get(self, user_id):
        """Get user by id"""
        pass

    def put(self, user_id):
        """update user by id """
        pass

    def delete(self, user_id):
        """delete  user using id"""
        pass


@user_namespace.route('/user/<int:user_id>/course/<int:course_id>/')
class GetSpecificCourseByUser(Resource):
    def get(self, user_id, course_id):
        """Get users.py specific course"""
        pass


@user_namespace.route('/user/<int:user_id>/courses.py')
class UserCourses(Resource):
    def get(self, user_id):
        """
        Get all specific courses.py for a user
        :param user_id:
        :return:
        """
        pass


@user_namespace.route('/course/status/<int:course_id>')
class UpdateCourseStatus(Resource):
    def patch(self, course_id):
        """
        Update an order's status
        :param course_id:
        :return:
        """
        pass

@user_namespace.route('/user/gpa/<int:user_id>')
class GetGPA(Resource):
    def patch(self, user_id):
        """
        get user gpa
        """
        pass