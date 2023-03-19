from flask_restx import Resource, Namespace, fields

from ..models.users import User
from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

user_namespace = Namespace('user', description="Namespace for user")

user_model = user_namespace.model(
    'User', {
        'name': fields.String(description="name of the user"),
        'is_staff': fields.Boolean(description="staff type"),
        'is_admin': fields.Boolean(description="admin status"),
        'is_active': fields.Boolean(description=" active status")
    }
)


@user_namespace.route('/')
class UserGetCreate(Resource):
    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self):
        """ Get all users.py"""
        logged_user = User.query.filter_by(email=get_jwt_identity()).first()
        if logged_user.is_admin:
            users = User.query.all()
            return users, HTTPStatus.OK
        else:
            return {"Failed": "You do not have permission to do this operation"}, HTTPStatus.FORBIDDEN


@user_namespace.route('/students')
class GetStudents(Resource):

    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self):
        """ Get all students.py"""
        logged_user = User.query.filter_by(email=get_jwt_identity()).first()
        if logged_user.is_admin is True or logged_user.is_staff is True:
            users = User.query.filter_by(is_staff=False, is_admin=False).all()
            return users, HTTPStatus.OK
        else:
            return {"Failed": "You do not have permission to do this operation"}, HTTPStatus.FORBIDDEN


@user_namespace.route('/user/<int:user_id>')
class GetUpdateDeleteUser(Resource):

    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self, user_id):
        """Get user by id"""
        user = User.get_by_id(user_id)
        if user is not None:
            return user, HTTPStatus.OK

    @user_namespace.expect(user_model)
    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def patch(self, user_id):
        """update user by id """
        data = user_namespace.payload
        user = User.get_by_id(user_id)
        if user is not None:
            user.name = data['name']
            user.is_active = data['is_active']
            user.is_staff = data['is_staff']
            user.is_admin = data['is_admin']
            user.save()
            return user, HTTPStatus.OK

    @jwt_required()
    def delete(self, user_id):
        """delete  user using id"""
        user = User.get_by_id(user_id)
        if user is not None:

            logged_user = User.query.filter_by(email=get_jwt_identity()).first()

            if logged_user.is_staff is False or logged_user.is_admin is False:
                return {"failed": "You do not have the permissions to do this operation"}, HTTPStatus.FORBIDDEN
            elif logged_user.email is user.email:
                return {"failed": "You can not delete your account please contact admin"}, HTTPStatus.FORBIDDEN
            else:
                user.delete()
                return {"Success": "Deleted user"}, HTTPStatus.NO_CONTENT



