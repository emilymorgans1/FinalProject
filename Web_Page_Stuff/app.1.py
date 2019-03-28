import os
import io
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from urllib.request import urlopen
import string
import datetime

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name = "dfcrqmhfx",
    api_key = "742959647143268",
    api_secret ="I7xzTiB7xDlknAdyL5TEc5PQycM")

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from keras import backend as K

from google.cloud import translate
target = 'es'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "MyProject-87540abb832b.json"
translate_client = translate.Client()

from flask import Flask, request, redirect, url_for, jsonify, render_template

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = None
graph = None


def load_model():
    global model
    global graph
    model = Xception(weights="imagenet")
    graph = K.get_session().graph

load_model()

def prepare_image(img):
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    # return the processed image
    return img


@app.route("/")
def index():
   """Return the homepage."""
   return render_template("index2.html")

#@app.route("/info")
#def info():

#    return render_template("info.html")

# @app.route('/')
# def index():
#     img = ""
#     return render_template("index.html",img=img)

@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        if request.files.get('img_file'):
            # read the file
            file = request.files['img_file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            now = datetime.datetime.now()
            cd = cloudinary.uploader.upload(file, folder = "rudsfinal")
            filepath= cd['url']
            image_size = (299, 299)
            im = ''

            with urlopen(filepath) as img:
                im = keras.preprocessing.image.load_img(img,
                                                    target_size=image_size,
                                                    grayscale=False)
            # preprocess the image and prepare it for classification
            image = prepare_image(im)
            
            global graph
            with graph.as_default():
                preds = model.predict(image)
                results = decode_predictions(preds)
                # print the results
                print(results)

                data["predictions"] = []

                # loop over the results and add them to the list of
                # returned predictions
                for (imagenetID, label, prob) in results[0]:
                    
    
                    translation = translate_client.translate(label, target_language=target)
  
                    r = {"label": label, "translation": translation["translatedText"]}
                    data["predictions"].append(r)


                # indicate that the request was a success
                data["success"] = True
        return jsonify(data)
        

# @app.route("/getfile", methods=['GET', 'POST'])
# def getFile():


#     model = None
#     graph = None


# def load_model():
#     global model
#     global graph
#     model = Xception(weights="imagenet")
#     graph = K.get_session().graph


# load_model()


#     # Load the saved image using Keras and resize it to the Xception
#     # format of 299x299 pixels
#     image_size = (299, 299)
#     im = keras.preprocessing.image.load_img(filepath,
#                                             target_size=image_size,
#                                             grayscale=False)

#     # preprocess the image and prepare it for classification
#     image = prepare_image(im)

#     global graph
#     with graph.as_default():
#         preds = model.predict(image)
#         results = decode_predictions(preds)
#         # print the results
#         print(results)

#         data["predictions"] = []

#         # loop over the results and add them to the list of
#         # returned predictions
#         for (imagenetID, label, prob) in results[0]:
            

#             translation = translate_client.translate(label, target_language=target)

#             r = {"label": label, "translation": translation["translatedText"]}
#             data["predictions"].append(r)


#         # indicate that the request was a success
#         data["success"] = True


#     return jsonify(data)

    

    #return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''

    #return render_template ("index.html")
    

if __name__ == "__main__":
    app.run(debug=True,port=8001)

