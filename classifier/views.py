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


def home(request):
    print(BASE_DIR)
    print("*******************")
    print(file_path)
    context={}
    return render(request,'classifier/index.html', context)

def predictImage(request):
    if request.method=='POST':
        propic = request.FILES['filePath']
       # fs=FileSystemStorage()
        #fs.save(propic.name,propic)
        modelpic=uploadPic(img1=propic)
        modelpic.save()
        print(modelpic.img1.url)
        x='.'+modelpic.img1.url
        print(x)
        IMG_SIZE = 224
        #imgpth=os.path.join(filepath)
        img= cv2.imread(x,cv2.IMREAD_COLOR)
        #img_array = cv2.imread(filepath,cv2.IMREAD_COLOR)

        img_array = cv2.cvtColor(img ,cv2.COLOR_BGR2RGB)
        new_array = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        check=new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

        prediction = loaded_model.predict([check])
        if(prediction[0][0]>prediction[0][1]):
            ans="Benign"
            score=prediction[0][0]
        else:
            ans="Malignant"
            score=prediction[0][1]

        context={'pic':modelpic,'ans':ans,'score':score}
        return render(request,'classifier/output.html',context)
    return render(request,'classifier/index.html')