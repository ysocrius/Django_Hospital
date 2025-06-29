from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user_choice, name='register_choice'),
    path('register/patient/', views.PatientRegistrationView.as_view(), name='register_patient'),
    path('register/doctor/', views.DoctorRegistrationView.as_view(), name='register_doctor'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
] 