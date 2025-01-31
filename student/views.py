from django.shortcuts import render,redirect

from django.views.generic import View,TemplateView,FormView,CreateView

from student.forms import StudentCreateForm,SignInForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,login,logout


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

        return render(request,"index.html")

   