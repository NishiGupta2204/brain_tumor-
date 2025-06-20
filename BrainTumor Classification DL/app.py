import os
import numpy as np
from PIL import Image
import cv2
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename 
from tensorflow.keras.models import Model #type: ignore
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout  #type: ignore
from tensorflow.keras.applications import VGG19  #type: ignore


base_model = VGG19(include_top=False, input_shape=(240,240,3))
x = base_model.output
flat=Flatten()(x)
class_1 = Dense(4608, activation='relu')(flat)
drop_out = Dropout(0.2)(class_1)
class_2 = Dense(1152, activation='relu')(drop_out)
output = Dense(2, activation='softmax')(class_2)
model_03 = Model(base_model.inputs, output)
model_03.load_weights('C:/Users/nishi/Brain Tumour/BrainTumor Classification DL/vgg_unfrozen.h5')
app = Flask(__name__)

print('Model loaded. Check http://127.0.0.1:5000/')


def get_className(classNo):
	if classNo==0:
		return "No Brain Tumor"
	elif classNo==1:
		return "Yes Brain Tumor"


def getResult(img_path):
    image = Image.open(img_path).convert('RGB')   
    image = image.resize((240, 240))                
    image = np.array(image)                        
    input_img = np.expand_dims(image, axis=0)       
    result = model_03.predict(input_img)            
    result01 = np.argmax(result, axis=1)[0]         
    return result01


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        value=getResult(file_path)
        result=get_className(value) 
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)