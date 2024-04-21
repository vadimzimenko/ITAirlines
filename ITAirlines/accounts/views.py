from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.utils import timezone

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class PersonalPageView(TemplateView):
    template_name = "accounts/personal_page.html"
    extra_context = {
        "time_now": timezone.now()
    }