# import unittest
# from .. import create_app
# from ..config.config import config_dict
# from ..models.users import User
# from ..utilities import db
# from flask_jwt_extended import create_access_token
#
# class UserTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app=create_app(config=config_dict['test'])
#         self.appctx=self.app.app_context()
#
#         self.appctx.push()
#
#         self.client=self.app.test_client()
#
#         db.create_all()
#
#
#     def tearDown(self):
#         db.drop_all()
#
#         self.app=None
#
#         self.appctx.pop()
#
#         self.client=None
#
#
#     def test_get_all_users(self):
#
#         token=create_access_token(identity='testuser')
#
#         headers={
#             "Authorization":f"Bearer {token}"
#         }
#
#         response=self.client.get('/users/students',headers=headers)
#
#         assert response.status_code == 200
#
#         assert response.json == []
#
#
#     def test_create_user(self):
#         data={
#             "size":"LARGE",
#             "quantity":3,
#             "flavour":"Test Flavour"
#         }
#
#         token=create_access_token(identity='testuser')
#
#         headers={
#             "Authorization":f"Bearer {token}"
#         }
#
#
#         response=self.client.post('/users',json=data,headers=headers)
#
#
#         assert response.status_code == 201
#
#         orders= User.query.all()
#
#         assert len(orders) == 1
