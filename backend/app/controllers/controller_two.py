from flask_restx import Namespace, Resource

api = Namespace('ControllerTwo', description='Controller Two operations')

@api.route('/')
class ControllerTwoResource(Resource):
    def get(self):
        return {"message": "Controller Two"}

