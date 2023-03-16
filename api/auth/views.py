from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

auth_namespace = Namespace('auth', description='a namespace for authentication')

signup_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description="User`s name"),
        'email': fields.String(required=True, description="User`s email address"),
        'password': fields.String(required=True, description="The users password")
    }
)
user_model = auth_namespace.model(
    'User',{
        'id': fields.Integer(),
        'name': fields.String(required=True, description="User`s name"),
        'email': fields.String(required=True, description="User`s email address"),
        'password_hash': fields.String(required=True, description="The users password"),
        'is_active':fields.Boolean(description="Shows if user is active"),
        'is_staff': fields.Boolean(description="Show if user is staff"),
        'is_admin': fields.Boolean(description="shows sif user is admin")

    }
)

@auth_namespace.route('/')
class HelloAuthentication(Resource):
    def get(self):
        return {"message": "Hello auth"}


@auth_namespace.route('/signup')
class SignUp(Resource):


    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """create user"""
        data = request.get_json()
        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
        )
        new_user.save()
        return new_user, HTTPStatus.CREATED


@auth_namespace.route('login')
class Login(Resource):
    def post(self):
        """generate a JWT"""
        pass
