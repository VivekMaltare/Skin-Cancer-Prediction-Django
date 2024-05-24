from django.test import TestCase

# Create your tests here.
import os
import cv2
import numpy as np
from keras.models import model_from_json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'model.json')
file_path2 = os.path.join(module_dir, 'model.h5')

# Load json and create model
json_file = open(file_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# Load weights into new model
loaded_model.load_weights(file_path2)
print("Loaded model from disk1")

IMG_SIZE = 224

# Ground truth labels for each image
ground_truth = {
    'img1.jpg': 'Benign',
    'img2.jpg': 'Malignant',
    # Add ground truth labels for remaining images
}

# Process 10 images
for i in range(1, 3):
    img_path = os.path.join(BASE_DIR, 'test_images', f'img{i}.jpg')
    if os.path.exists(img_path):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        new_array = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        check = new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        prediction = loaded_model.predict([check])
        if prediction[0][0] > prediction[0][1]:
            predicted_label = "Benign"
            score = prediction[0][0]
        else:
            predicted_label = "Malignant"
            score = prediction[0][1]
        
        # Compare with ground truth
        ground_truth_label = ground_truth.get(f'img{i}.jpg', 'Unknown')
        if ground_truth_label != 'Unknown':
            if predicted_label == ground_truth_label:
                match = "Correct"
            else:
                match = "Incorrect"
            print(f"Prediction for {img_path}: Predicted - {predicted_label}, Ground Truth - {ground_truth_label}, Match - {match}, Score - {score}")
        else:
            print(f"No ground truth label found for {img_path}")
    else:
        print(f"Image {img_path} not found.")