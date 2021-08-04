from django.db import models
from mycourse.models.courses import Course
from mycourse.models.customer import Customer
from mycourse.models.customer_course import CustomerCourse


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=500,null=False)
    payment_id = models.CharField(max_length=500,null=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    customer_course = models.ForeignKey(CustomerCourse,on_delete=models.CASCADE,null=True,blank=True)
    data = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)