from django.urls import path
from accounts.views import UserProfileView, set_theme_color

urlpatterns = [
    path('', UserProfileView.as_view(), name='user_profile'),
    path('theme/<str:color>/', set_theme_color, name='set_theme_color')

]