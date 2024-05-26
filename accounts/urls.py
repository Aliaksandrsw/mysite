from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', ProfileViews.as_view(), name='users-profile'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
]