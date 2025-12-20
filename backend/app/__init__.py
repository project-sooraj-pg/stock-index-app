from flask import Flask
from flask_restx import Api
from app.controllers.controller_one import api as controller_one_ns
from app.controllers.controller_two import api as controller_two_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, title="Stock Index API", version="1.0", description="API for Stock Index App")
    api.add_namespace(controller_one_ns, path="/api/one")
    api.add_namespace(controller_two_ns, path="/api/two")
    return app

