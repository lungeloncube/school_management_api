from flask import Flask
from flask_restx import Api
from .user.views import user_namespace
from .auth.views import auth_namespace
from .course.views import course_namespace
from .course_work.views import course_work_namespace
from .config.config import config_dict
from .utilities import db
from .models.courses import Course
from .models.users_to_courses import UserToCourse
from .models.course_work import CourseWork
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    api = Api(app)
    api.add_namespace(user_namespace, path='/users')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(course_work_namespace, path='/course_work')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'user': User,
            'course': Course,
            'course_work': CourseWork,
            'user_to_course': UserToCourse

        }

    return app
