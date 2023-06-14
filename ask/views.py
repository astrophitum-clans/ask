import random
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Question, Answer


# Create your views here.

def get_random_question(user):
    """Return a random question where the author is not the current user and he`s not been asked this question before"""
    return Question.objects.exclude(author=user).exclude(answers__author=user).order_by('?').first()

    # ToDo: Optimize this method


class LastAnswerCheckMixin:
    """Mixin: redirect to an answer if current user`s last answer was earlier LAST_ANSWER_TIMEDELTA"""

    # ToDo: add next to redirect

    def get(self, request, *args, **kwargs):

        LAST_ANSWER_TIMEDELTA = 3  # hours
        random_question = get_random_question(request.user)

        if random_question and (
                not request.user.last_answer  # is None - first time show it
                or datetime.now() - request.user.last_answer.replace(tzinfo=None) >
                timedelta(hours=LAST_ANSWER_TIMEDELTA)
        ):
            return redirect(reverse_lazy('answer_to_question', kwargs={'pk': random_question.id}))

        return super().get(request, *args, **kwargs)


class HomePageView(LoginRequiredMixin, LastAnswerCheckMixin, TemplateView):
    """Home page view"""
    template_name = 'home.html'


class FaqPageView(LoginRequiredMixin, LastAnswerCheckMixin, TemplateView):
    """FAQ page view"""
    template_name = 'ask/faq.html'


class QuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Questions list view"""
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/question_list.html'


class MyQuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Only current user`s questions list view"""
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/my_question_list.html'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)


class QuestionDetailView(LoginRequiredMixin, LastAnswerCheckMixin, DetailView):
    """Question detail vies"""
    model = Question
    template_name = 'ask/question_detail.html'


class QuestionCreateView(LoginRequiredMixin, LastAnswerCheckMixin, CreateView):
    """Create question view"""
    model = Question
    template_name = 'ask/question_create.html'
    fields = ['text']
    success_url = reverse_lazy('my_question_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnswerToQuestionView(LoginRequiredMixin, CreateView):
    """Answer to question view"""
    model = Answer
    template_name = 'ask/question_answer.html'
    fields = ['text']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """Add question to context"""
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """Set current author, question and add answer`s datetime to current user"""
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        self.update_user_last_answer_time(self.request.user)
        return super().form_valid(form)

    def update_user_last_answer_time(self, user):
        user.last_answer = datetime.now()
        user.save()


class AnswerListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Current user answers view"""
    model = Question
    context_object_name = 'answer_list'
    template_name = 'ask/answer_list.html'

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)


class AnswerToMyQuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Only current user`s questions list view"""
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/answer_to_my_question_list.html'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)
