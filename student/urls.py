from django.urls import path

from student import views


urlpatterns=[
   path("register/",views.StudentRegistrationView.as_view(),name="student-register"),
   path("signin/",views.SignInView.as_view(),name="signin"),
   path('index/',views.IndexView.as_view(),name="index"),
   path('courses/<int:pk>/',views.CourseDetailView.as_view(),name="course-detail"),
   path('courses/<int:pk>/add-to-cart/',views.AddToCartView.as_view(),name="add-to-cart"),
]