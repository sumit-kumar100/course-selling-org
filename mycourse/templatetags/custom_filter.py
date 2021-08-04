import math
from django import template
from mycourse.models.customer_course import CustomerCourse
from mycourse.models.courses import Course
from mycourse.models.customer import Customer
register = template.Library()


@register.filter(name="rupee")
def rupee(price):
    return '₹'+ str(price)


@register.filter(name='list_price')
def list_price(price,discount):
    less_discount = price*discount/100
    return math.floor(price-less_discount)


@register.filter(name='truncate')
def truncate(title):
    if len(title)<=58:
        return title
    else:
        return title[:46]+'...'


@register.filter(name='is_customer_course')
def is_customer_course(course,customer):
    if CustomerCourse.objects.filter(customer = Customer(customer) , course = Course(course.id)):
        return True
    else:
        return False


@register.filter(name='mycourses_length')
def mycourses_length(customer):
    cs = CustomerCourse.objects.filter(customer=Customer(customer))
    return len(cs)


@register.filter(name='is_free')
def is_free(course):
    videos = course.video_set.all()
    for i in videos:
        if not i.is_preview:
            return False
    return True