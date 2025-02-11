from django.shortcuts import render,redirect

from django.views.generic import View,TemplateView,FormView,CreateView

from student.forms import StudentCreateForm,SignInForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout

from instructor.models import Course,Cart,Order,Lesson,Module

from django.db.models import Sum


import razorpay


RZP_KEY_ID = "rzp_test_Y7sGikK5i973t2"

RZP_KEY_SECRET="qszlYhnYkYlosCluUfrlKOtU"



# Create your views here

class StudentRegistrationView(CreateView):

   template_name="student_register.html"

   form_class=StudentCreateForm

   success_url=reverse_lazy("signin")

   

class SignInView(FormView):

    # form view

    template_name="signin.html"

    form_class=SignInForm

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=SignInForm(form_data)

        if form_instance.is_valid():

            data = form_instance.cleaned_data

            uname= data.get("username")

            pwd = data.get("password")

            user_obj=authenticate(request,username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)
                

                return redirect("index")
            
            else:
                
                return redirect("signin")



class IndexView(View):   

    def get(self,request,*args,**kwargs):

        all_courses=Course.objects.all()

        purchased_courses=Order.objects.filter(student=request.user).values_list("course_objects",flat=True)

        print("=============",purchased_courses)


        return render(request,"index.html",{"courses":all_courses,"purchased_courses": purchased_courses})

   

class CourseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        course_instance=Course.objects.get(id=id)

        return render(request,"course_detail.html",{"coursedetail":course_instance})
    

class AddToCartView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        course_instance=Course.objects.get(id=id)

        user_instance=request.user

        #Cart.objects.create(course_object=course_instance,user=user_instance)

        cart_instance,created=Cart.objects.get_or_create(course_object=course_instance,user=user_instance)

        print(created)

        return redirect("index")



class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.all()

        cart_total=qs.values("course_object__price").aggregate(total=Sum("course_object__price")).get("total")

        print("===========",cart_total)

        #  or  qs=Cart.objects.filter(user=request.user)

        return render(request,"cart-summary.html",{"carts":qs,"basket_total":cart_total})
    

class CartItemDeleteView(View):

     def get(self,request,*args,**kwargs):

       id=kwargs.get("pk")

       Cart.objects.get(id=id).delete()

       return redirect("cart-summary")
     

class CheckoutView(View):

    def get(self,request,*args,**kwargs):

        cart_items=request.user.basket.all()

        order_total=sum([ci.course_object.price for ci in cart_items])

        order_instance=Order.objects.create(student=request.user,total=order_total)

        for ci in cart_items:

            order_instance.course_objects.add(ci.course_object)

            ci.delete()

        order_instance.save()


        if order_total>0:
            # authenticate
            client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))
            # create a order
            data = { "amount": int(order_total*100), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            print(payment,"=============")



        return redirect("index")



class MyCoursesView(View):

    def get(self,request,*args,**kwargs):

         qs = request.user.purchase.all()

         return render(request,"mycourses.html",{"orders": qs})


#localhost:8000/students/courses/1/watch?module=1&lesson5

#?- optional query parameter

class LessonDetailView(View):

    def get(self,request,*args,**kwargs):

        course_id=kwargs.get("pk")

        course_instance=Course.objects.get(id=course_id)

       # extracting lesson

       #request.GET={"module 2",lesson:5}

        # if "module" in request.GET:

        #     module_id = request.GET.get("module")

        # else:

        #     module_id =1

        # if "lesson" in request.GET:

        #     lesson_id = request.GET.get("lesson")

        # else:

        #     lesson_id =1

        # or

        module_id=request.GET.get("module") if "module" in request.GET else course_instance.modules.first().id

        module_instance= Module.objects.get(id=module_id,course_object=course_instance)

        lesson_id=request.GET.get("lesson") if "lesson" in request.GET else module_instance.lessons.first().id

        lesson_instance=Lesson.objects.get(id=lesson_id,module_object=module_instance)

        return render(request,"lesson_detail.html",{"coursedetail":course_instance,"lesson": lesson_instance})




