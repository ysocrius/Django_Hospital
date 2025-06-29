from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard'),
    path('patient/', views.PatientDashboardView.as_view(), name='patient_dashboard'),
    path('doctor/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
] 