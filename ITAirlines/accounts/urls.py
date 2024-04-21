from django.urls import path
from django.contrib.auth.decorators import login_required

from accounts import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("personal_page/", login_required(views.PersonalPageView.as_view()), name="personal_page"),
]