from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
import time
from mycourse.models.courses import Course,Video
from mycourse.models.customer import Customer
from mycourse.models.customer_course import CustomerCourse
# Create your views here.
def index(requests):
    return render(requests,'index.html',{'courses':Course.objects.all()})


def mycourse(requests):
    customer = requests.session.get('customer') 
    mycourse = CustomerCourse.objects.filter(customer=Customer(customer)) if customer else []
    return render(requests,'mycourse.html',{'mycourses':mycourse})


def myprofile(requests):
    customer = requests.session.get('customer')
    customer_data = Customer.objects.get(id=customer)
    password_request = requests.GET.get('edit')
    if password_request is None:
        password_request = None
    return render(requests,'myprofile.html',{'customer_data':customer_data,'password_request':password_request})


def edit(requests):
    if requests.method == 'POST':
        first_name = requests.POST['first_name']
        last_name = requests.POST['last_name']
        mail = requests.POST['mail']
        phone_number = requests.POST['phone_number']
        customer_id = requests.POST['id']

        if len(phone_number)<10 or len(phone_number)>10:
            messages.error(requests,'invalid phone number')
            return redirect('/my-profile/')

        customer_dt = Customer.objects.get(id=customer_id)
        customer_dt.first_name = first_name
        customer_dt.last_name = last_name
        customer_dt.mail = mail
        customer_dt.phone = phone_number
        customer_dt.save()
        messages.success(requests,'Successfully edit profile')
        return redirect('/my-profile/')


def edit_password(requests):
    customer = requests.session.get('customer')
    customer_dt = Customer.objects.get(id=customer)
    if requests.method == "POST":
        last_password = requests.POST['last_password']
        new_password = requests.POST['new_password']
        confirm_password = requests.POST['confirm_new_password']

        if last_password != customer_dt.password:
            messages.error(requests,"last password didn't match ")
            return HttpResponseRedirect('/my-profile/?edit=password')
        elif new_password != confirm_password:
            messages.info(requests,'You must enter the same password twice in order to confirm it')
            return HttpResponseRedirect('/my-profile/?edit=password')
        elif len(new_password)<=8:
            messages.info(requests,'New Password must include 8 characters')
            return redirect('/my-profile/?edit=password')
        else:
            customer_dt.password = new_password
            customer_dt.save()
            messages.success(requests,'Passowrd updated succesfully')
            return HttpResponseRedirect('/my-profile/')
        

def all_courses(requests):
    return render(requests,'index.html',{'courses':Course.objects.all()})


def search(requests):
    if requests.method == "GET":
        query = requests.GET['query']
        all_courses = Course.objects.all()
        query_courses = []
        for course in all_courses:
            print(str(course.name))
            print(query)
            if query.capitalize() in str(course.name) or query.lower() in str(course.name) or query.upper() in str(course.name):
                query_courses.append(course)
            else:
                pass
    print(query_courses)
    return render(requests,'index.html',{'query_courses':query_courses})


def course_search(requests):
    searched_course = requests.GET['selected-course']
    courses = Course.objects.all()
    free_courses = []
    paid_courses = []
    for i in courses:
        videos = i.video_set.all()
        free = False
        for j in videos:
            if j.is_preview is True:
                free = True
            else:
                price = i.price
                discount = i.discount
                discount_amt = price*discount/100
                final_price = price-discount_amt
                if final_price == 0:
                    free = True
                else:
                    free = False
                    break
        if free is True:
            free_courses.append(i)
        else:
            paid_courses.append(i)
    if searched_course == 'Select Courses':
        return redirect('/')
    elif searched_course == 'All Courses':
        data = Course.objects.all()
        return render(requests,'index.html',{'data':data})
    elif searched_course == 'Free Courses':
        data = free_courses
        return render(requests,'index.html',{'data':data})
    else:
        data = paid_courses
        return render(requests,'index.html',{'data':data})


def courses(requests,slug):
    courses = Course.objects.get(slug=slug)
    try:
        discount = courses.discount
        price = courses.price
        discount_amt = price*discount/100
        final_amt = price-discount_amt
    except:
        final_amt = 100
    ''' Important Video model has Foreign key related to specific_course.
        we are getting videos of a specific_course using below method.
        i.e, main_course_name.name_of_related_foreign_model_in_lower_case.set.all().
        all() here refers to all the objects of video.
    ''' 
    #videos = courses.video_set.all()
    serial_no = requests.GET.get('episode')
    if serial_no is None:
        serial_no = 1

    requested_video = Video.objects.get(course=courses,serial_no=serial_no)
    customer = requests.session.get('customer')

    #Checking is this customer Course 
    is_customer_course = False
    try:
        CustomerCourse.objects.get(customer = Customer(customer) , course = Course(courses.id))
        is_customer_course = True
    except:
        is_customer_course = False
    

    if requested_video.is_preview is False:
        if not requests.session.get('customer'):
            return redirect('/login/')
        elif (final_amt == 0):
            data = CustomerCourse.objects.create(customer=Customer(customer),course=Course(courses.id))
            data.save()
            time.sleep(4)
            return redirect('/')
        else:
            try:
                CustomerCourse.objects.get(customer = Customer(customer) , course = Course(courses.id))
            except:
                return redirect('checkout',slug=slug)
    return render(requests,'courses.html',{'courses':courses,'requested_video':requested_video,'is_customer_course':is_customer_course})


def signup(requests):
    return render(requests,'signup.html')


def signup_user(requests):
    if requests.method == 'POST':
        first_name = requests.POST['first_name']
        last_name = requests.POST['last_name']
        mail = requests.POST['mail']
        password = requests.POST['password']
        if Customer.objects.filter(mail=mail):
            messages.error(requests,'mail already exist')
            return redirect('/signup/')
        elif len(password)<=8:
            messages.info(requests,'Password must include 8 characters')
            return redirect('/signup/')
        else:
            x = Customer.objects.create(first_name=first_name,last_name=last_name,mail=mail,password=password)
            x.save()

            customer = Customer.objects.get(mail=mail,password=password)
            requests.session['customer'] = customer.id
    return redirect('/')


def login(requests):
    return render(requests,'login.html')


def login_user(requests):
    mail = requests.POST["mail"]
    password = requests.POST['password']
    if Customer.objects.filter(mail=mail,password=password):
        customer = Customer.objects.get(mail=mail,password=password)
        requests.session['customer'] = customer.id
        return redirect('/')
    else:
        messages.info(requests,'email or password is incorrect')
        return redirect('/login/')


def logout(requests):
    del requests.session['customer']
    return redirect('/')


def checkout(requests,slug):
    courses = Course.objects.get(slug=slug)
    discount = courses.discount
    price = courses.price
    discount_amt = price*discount/100
    final_amt = price-discount_amt
    customer = requests.session.get('customer')
    if not requests.session.get('customer'):
        return redirect('/login/')
    elif (final_amt == 0):
        data = CustomerCourse.objects.create(customer=Customer(customer),course=Course(courses.id))
        data.save()
        time.sleep(4)
        return redirect('/')
    else:
        customer = requests.session.get('customer')
        details = Customer.objects.get(id=customer)
        return render(requests,'checkout.html',{'course':Course.objects.get(slug=slug),'details':details})


def order(requests):
    customer = requests.session.get('customer')
    customer_data = Customer.objects.get(id=customer)
    if requests.method == 'POST':
        phone_number = requests.POST['phone_number']
        course_id = requests.POST['course_id']
        mail = requests.POST['mail']
        course_slug = requests.POST['course_slug']
        if len(phone_number)<10:
            messages.info(requests,'invalid phone number')
            return redirect('/checkout/{}/'.format(course_slug))
        elif customer_data.mail != mail:
            messages.error(requests,'Login mail required')
            return redirect('/checkout/{}/'.format(course_slug))
        else:
            x = CustomerCourse.objects.create(customer=Customer(customer),course=Course(int(course_id)))
            x.save()
            customer_data.phone = phone_number
            customer_data.save()
            return redirect('/') 




            '''returnurl = requests.META['PATH_INFO']
            return redirect('/login/?return_url={}'.format(returnurl))'''


