from django.db import models

# Create your models here.

class uploadPic(models.Model):
    img1=models.ImageField(null=True,blank=True,upload_to="images/")