from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import PatientRegistrationForm, DoctorRegistrationForm


def register_user_choice(request):
    """View to let user choose between patient and doctor registration"""
    return render(request, 'users/register_choice.html')


class PatientRegistrationView(CreateView):
    """View for patient registration"""
    form_class = PatientRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'Patient'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Patient account created successfully. You can now login.')
        return response


class DoctorRegistrationView(CreateView):
    """View for doctor registration"""
    form_class = DoctorRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'Doctor'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Doctor account created successfully. You can now login.')
        return response


@method_decorator(sensitive_post_parameters(), name='post')
@method_decorator(csrf_protect, name='dispatch')
class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        
        # Check if user has a user_type or is a superuser
        user = self.request.user
        if not hasattr(user, 'user_type') or not user.user_type:
            if not user.is_superuser:
                # Log out and show message for regular users without type
                messages.warning(self.request, 'Your account does not have a user type assigned. Please contact an administrator.')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return the success URL."""
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        else:
            return reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    """Custom logout view that allows both GET and POST requests"""
    next_page = 'login'
    http_method_names = ['get', 'post']  # Allow both GET and POST requests
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have successfully logged out.')
        return super().dispatch(request, *args, **kwargs)
