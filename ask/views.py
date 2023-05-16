from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse, reverse_lazy

from .models import Question, Answer


# Create your views here.


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/question_list.html'


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'ask/question_detail.html'


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'ask/question_create.html'
    fields = ['text']
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnswerToQuestionView(LoginRequiredMixin, CreateView):
    model = Answer
    template_name = 'ask/question_answer.html'
    fields = ['text']
    success_url = reverse_lazy('question_list')

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnswerListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'answer_list'
    template_name = 'ask/answer_list.html'

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)
