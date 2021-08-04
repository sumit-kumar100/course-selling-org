from django.db import models
from mycourse.models.courses import Course
from mycourse.models.customer import Customer


class CustomerCourse(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    date = models.DateTimeField(auto_now_add=True)