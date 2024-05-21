from django.shortcuts import render
import matplotlib.pyplot as plt
import cv2
import numpy as np
from keras.models import model_from_json
import os
from .models import uploadPic
from django.core.files.storage import FileSystemStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'model.json')
file_path2 = os.path.join(module_dir, 'model.h5')

# load json and create model
json_file = open(file_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(file_path2)
print("Loaded model from disk1")
# Create your views here.

import logging

try:
    # Get the logger named 'django'
    logger = logging.getLogger('django')
    print("Logger loaded successfully")
except Exception as e:
    print(f"Error loading logger: {e}")

def home(request):
    print(BASE_DIR)
    print("*******************")
    print(file_path)
    context={}
    return render(request,'classifier/index.html', context)

def predictImage(request):
    logger.info("predictImage view called")
    
    if request.method == 'POST':
        propic = request.FILES.get('filePath')
        
        if propic is None:
            logger.error("No image file provided in the request.")
            return render(request, 'classifier/index.html', {'error': 'No image file provided'})
        
        logger.info(f"Image file received: {propic.name}")

        # Save the image file to the model
        modelpic = uploadPic(img1=propic)
        modelpic.save()
        logger.info(f"Image file saved at: {modelpic.img1.url}")

        # Prepare the image for prediction
        x = '.' + modelpic.img1.url
        IMG_SIZE = 224

        try:
            img = cv2.imread(x, cv2.IMREAD_COLOR)
            if img is None:
                logger.error("Failed to read the image file.")
                return render(request, 'classifier/index.html', {'error': 'Failed to read the image file'})

            img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            new_array = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            check = new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

            logger.info("Image preprocessing successful.")
        except Exception as e:
            logger.error(f"Error during image preprocessing: {e}")
            return render(request, 'classifier/index.html', {'error': 'Error during image preprocessing'})

        # Perform prediction
        try:
            prediction = loaded_model.predict([check])
            logger.info("Prediction successful.")

            if prediction[0][0] > prediction[0][1]:
                ans = "Benign"
                score = prediction[0][0]
            else:
                ans = "Malignant"
                score = prediction[0][1]

            context = {'pic': modelpic, 'ans': ans, 'score': score}
            logger.info(f"Prediction result: {ans} with score {score}")
            return render(request, 'classifier/output.html', context)
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return render(request, 'classifier/index.html', {'error': 'Error during prediction'})

    return render(request, 'classifier/index.html')