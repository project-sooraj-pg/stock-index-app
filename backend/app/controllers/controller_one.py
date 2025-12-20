from flask_restx import Namespace, Resource

api = Namespace('ControllerOne', description='Controller One operations')

@api.route('/')
class ControllerOneResource(Resource):
    def get(self):
        return {"message": "Controller One"}

