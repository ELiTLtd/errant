from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

class Annotate(Resource):
    def get(self):
        return {"message": "Hello world!"}, 200

api.add_resource(Annotate, "/annotate")

app.run(debug=True)
