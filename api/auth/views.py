from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)

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
    'User', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description="User`s name"),
        'email': fields.String(required=True, description="User`s email address"),
        'password_hash': fields.String(required=True, description="The users password"),
        'is_active': fields.Boolean(description="Shows if user is active"),
        'is_staff': fields.Boolean(description="Show if user is staff"),
        'is_admin': fields.Boolean(description="shows sif user is admin")

    }
)

login_model = auth_namespace.model(
    'login', {
        'email': fields.String(required=True, description="Email address used for signup"),
        'password': fields.String(required=True, description="A password")
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """create user"""
        data = request.get_json()
        users = User.query.filter_by(email=data['email']).all()
        if len(users) < 1:
            new_user = User(
                name=data.get('name'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
            )
            new_user.save()
            return new_user, HTTPStatus.CREATED
        else:
            return {"failed": "User already exist"}, HTTPStatus.CONFLICT


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """Generate a JWT"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        else:
            return {"Failed": "Account email or password incorrect!"}, HTTPStatus.BAD_REQUEST


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        email = get_jwt_identity()
        access_token = create_access_token(identity=email)

        return {'access_token': access_token}, HTTPStatus.OK
