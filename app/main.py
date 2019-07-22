from flask import Flask
from flask_restful import Api, Resource, reqparse
from errant import annotate

app = Flask(__name__)
api = Api(app)

class Annotate(Resource):
    def get(self):
        return {"message": "Hello world!"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("original")
        parser.add_argument("corrected")
        args = parser.parse_args()
        response = {"m2": annotate(args["original"], args["corrected"]),
                    "original": args["original"],
                    "corrected": args["corrected"]}
        return response, 200

api.add_resource(Annotate, "/annotate")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
