from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView

from .models import Question, Answer


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'


class QuestionListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/question_list.html'


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'ask/question_detail.html'
