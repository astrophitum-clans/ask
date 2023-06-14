from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model


# Create your views here.

class UserProfileView(TemplateView):
    template_name = 'account/profile.html'


@login_required
def set_theme_color(request, color):
    user = get_user_model().objects.get(pk=request.user.pk)
    if color == 'light':
        user.light_theme = True
    elif color == 'dark':
        user.light_theme = False
    user.save()
    return redirect(reverse_lazy('user_profile'))
