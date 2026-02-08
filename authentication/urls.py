from django.urls import path, include
from .views import *
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('register/', register_view, name="register"),
    path('verify_otp/', verify_otp_view, name="verify_otp"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('complete_profile/', complete_profile_view, name='complete_profile'),
    path('profile/', profile_view, name='profile'),
]
