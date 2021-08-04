from django.db import models


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=False)
    slug = models.CharField(max_length=150,null=False,unique=True)
    description = models.TextField(max_length=500,null=True)
    price = models.FloatField(null=True,blank=True)
    discount = models.IntegerField(null=True,blank=True,default=0)
    image = models.ImageField(upload_to='course/images/')
    date = models.DateTimeField(auto_now_add=True)
    related_file = models.FileField(upload_to='course/files/')
    length = models.FloatField(null=False)
    is_active = models.BooleanField(default=False)  


class Tagline(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)


class Prerequisite(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)


class Learning(models.Model):
    description = models.CharField(max_length=500,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)


class Video(models.Model):
    serial_no = models.IntegerField(null=False)
    video_title = models.CharField(max_length=100,null=False)
    video_url = models.CharField(max_length=100,null=False)
    video_img = models.CharField(max_length=500,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    is_preview = models.BooleanField(default=False)
