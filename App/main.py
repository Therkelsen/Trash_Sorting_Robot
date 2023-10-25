from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from roboflow import Roboflow
import base64
import cv2

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'msg': 'Api is working'}


api.add_resource(HelloWorld, '/helloworld')


rf = Roboflow(api_key="e6vqYw2hVrLBzvqxJoQc")
project = rf.workspace().project("taco-trash-annotations-in-context")
model = project.version(16).model

image_post_args = reqparse.RequestParser()
image_post_args.add_argument(
    "encodedImage", type=str, help="you didnt send encoded base64 image", required=True)


class UploadImage(Resource):
    def post(self):
        args = image_post_args.parse_args()
        img_base64 = args.encodedImage
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.b64decode(img_base64))
            result = model.predict("imageToSave.png").json()
        print(result)

        return{"result": result}


api.add_resource(UploadImage, "/uploadImage")


if __name__ == '__main__':
    app.run(debug=True)
