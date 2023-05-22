import random
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Question, Answer


# Create your views here.

def get_random_question(request):
    """Return a random question where the author is not the current user and he`s not been asked this question before"""
    return Question.objects.exclude(author=request.user).exclude(answers__author=request.user).order_by('?').first()

    # ToDo: Optimize this method


class LastAnswerCheckMixin:
    """Mixin that redirects to an answer if the last answer was earlier LAST_ANSWER_TIMEDELTA"""

    def get(self, request, *args, **kwargs):

        LAST_ANSWER_TIMEDELTA = timedelta(minutes=1)

        if get_random_question(request) is not None and (
                not request.user.last_answer
                or datetime.now() - request.user.last_answer.replace(tzinfo=None) > LAST_ANSWER_TIMEDELTA
        ):
            return redirect(reverse_lazy('answer_to_question', kwargs={'pk': get_random_question(request).id}))
        else:
            return super().get(request, *args, **kwargs)


class HomePageView(LoginRequiredMixin, LastAnswerCheckMixin, TemplateView):
    template_name = 'home.html'


class QuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/question_list.html'


class QuestionDetailView(LoginRequiredMixin, LastAnswerCheckMixin, DetailView):
    model = Question
    template_name = 'ask/question_detail.html'


class QuestionCreateView(LoginRequiredMixin, LastAnswerCheckMixin, CreateView):
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
        """Set current author, question and add answer`s datetime to current user"""
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        self.request.user.last_answer = datetime.now()
        self.request.user.save()
        return super().form_valid(form)


class AnswerListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    model = Question
    context_object_name = 'answer_list'
    template_name = 'ask/answer_list.html'

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)
