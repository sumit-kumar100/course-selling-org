"""courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mycourse import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('courses/<str:slug>/',views.courses),
    path('my-courses/',views.mycourse),
    path('my-profile/',views.myprofile),
    path('my-profile/edit-my-profile/',views.edit),
    path('my-profile/edit-my-profile/edit=password/',views.edit_password),
    path('all-courses/',views.all_courses),
    path('all-courses/search/',views.search),
    path('courses/',views.course_search),
    path('signup/',views.signup),
    path('signup_user/',views.signup_user),
    path('login/',views.login),
    path('login_user/',views.login_user),
    path('logout/',views.logout),
    path('checkout/<str:slug>/',views.checkout,name='checkout'),
    path('order/',views.order)

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
