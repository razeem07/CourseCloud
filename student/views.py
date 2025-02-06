from django.shortcuts import render,redirect

from django.views.generic import View,TemplateView,FormView,CreateView

from student.forms import StudentCreateForm,SignInForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout

from instructor.models import Course,Cart

from django.db.models import Sum


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

        return render(request,"index.html",{"courses":all_courses})

   

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
     




