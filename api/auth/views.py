from flask_restx import Namespace, Resource

auth_namespace = Namespace('auth', description='a namespace for authentication')


@auth_namespace.route('/')
class HelloAuthentication(Resource):
    def get(self):
        return {"message": "Hello auth"}


@auth_namespace.route('/signup')
class SignUp(Resource):
    def post(self):
        """create user"""
        pass


@auth_namespace.route('login')
class Login(Resource):
    def post(self):
        """generate a JWT"""
        pass
