from django.contrib import admin
from mycourse.models.courses import Course,Tagline,Prerequisite,Learning,Video
from mycourse.models.customer import Customer
from mycourse.models.customer_course import CustomerCourse
from mycourse.models.payment import Payment
# Register your models here.

class TaglineAdmin(admin.TabularInline):
    model = Tagline


class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite


class LearningAdmin(admin.TabularInline):
    model = Learning
  

class VideoAdmin(admin.TabularInline):
    model = Video


class CourseAdmin(admin.ModelAdmin):
    inlines = [TaglineAdmin,PrerequisiteAdmin,LearningAdmin,VideoAdmin]





admin.site.register(Course,CourseAdmin)
admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(CustomerCourse)