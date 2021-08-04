from django.db import models


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    mail = models.EmailField(unique=True,null=False)
    password = models.CharField(max_length=50,null=False)
    phone = models.IntegerField(null=True,blank=True)

