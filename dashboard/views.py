from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


@login_required
def dashboard_redirect(request):
    """Redirect to appropriate dashboard based on user type"""
    user = request.user
    
    # Handle superuser or users without user_type
    if user.is_superuser or not hasattr(user, 'user_type') or not user.user_type:
        # Return a basic dashboard for superusers or users without a type
        return render(request, 'dashboard/admin_dashboard.html')
        
    if user.is_patient():
        return redirect('patient_dashboard')
    elif user.is_doctor():
        return redirect('doctor_dashboard')
    else:
        # Default redirect if user type is not recognized
        return redirect('login')


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for patients"""
    template_name = 'dashboard/patient_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Check if user is a patient before accessing the view"""
        if not request.user.is_patient():
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    

class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for doctors"""
    template_name = 'dashboard/doctor_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Check if user is a doctor before accessing the view"""
        if not request.user.is_doctor():
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
