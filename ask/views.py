import random
from datetime import datetime, timedelta

import openai
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy

from django_project import settings
from .models import Question, Answer
from .tasks import ask_ai_task
from .utils import LastAnswerCheckMixin


# Create your views here.

class HomePageView(LoginRequiredMixin, LastAnswerCheckMixin, TemplateView):
    """Home page view"""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_questions'] = Question.objects.all()[:6].prefetch_related('author')
        context['top_questions'] = Question.objects.all().annotate(like_count=Count('like')).order_by('-like_count') \
            [:6].prefetch_related('author')
        return context


class FaqPageView(LoginRequiredMixin, LastAnswerCheckMixin, TemplateView):
    """FAQ page view"""
    template_name = 'ask/faq.html'


class QuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Questions list view"""
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/question_list.html'

    def get_queryset(self):
        return Question.objects.all().prefetch_related('author', 'like', 'unlike')


class MyQuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Only current user`s questions list view"""
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/my_question_list.html'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user).prefetch_related('author', 'like', 'unlike')


class QuestionDetailView(LoginRequiredMixin, LastAnswerCheckMixin, DetailView):
    """Question detail vies"""
    model = Question
    template_name = 'ask/question_detail.html'

    def get_context_data(self, **kwargs):
        """Add performance: answers to context"""
        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.kwargs['pk']).prefetch_related('author', 'like',
                                                                                                'unlike')
        context['has_ai_answer'] = Answer.objects\
            .filter(author__is_ai=True)\
            .filter(question__id=self.kwargs['pk'])\
            .exists()
        return context

    def get_object(self, queryset=None):
        question = super().get_object(queryset=queryset)
        question.new_answers_count = 0
        question.save()
        return question


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
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """Set current author, question and add answer`s datetime to current user"""
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form.instance.question = question
        form.instance.author = self.request.user
        question.new_answers_count += 1
        question.save()
        self.update_user_last_answer_time(self.request.user)
        return super().form_valid(form)

    def update_user_last_answer_time(self, user):
        user.last_answer = datetime.now()
        user.save()


class AnswerListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Current user answers view"""
    model = Answer
    context_object_name = 'answer_list'
    template_name = 'ask/answer_list.html'

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user) \
            .prefetch_related('author', 'like', 'unlike',
                              'question', 'question__author', 'question__like', 'question__unlike')


class AnswerToMyQuestionListView(LoginRequiredMixin, LastAnswerCheckMixin, ListView):
    """Only current user`s questions list view"""
    model = Question
    context_object_name = 'question_list'
    template_name = 'ask/answers_to_my_question_list.html'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user).prefetch_related('author', 'like', 'unlike')


@login_required
def like(request):
    """Set/unset likes & unlikes to target"""
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id')
        choice = request.POST.get('choice')
        reversed_choice = 'unlike' if choice == 'like' else 'like'
        match request.POST.get('target'):
            case 'question':
                target_model = Question
            case 'answer':
                target_model = Answer
            case _:
                target_model = None

        if target_model and choice in 'like unlike'.split():
            target = get_object_or_404(target_model, pk=id)

            # # set reverse choice status
            reversed_status = 'checked' if user in getattr(target, reversed_choice).all() else 'unchecked'

            # set choice to model & its status
            if user in getattr(target, choice).all():  # ex: question.like.all()
                getattr(target, choice).remove(user)
                status = 'unchecked'
            else:
                getattr(target, choice).add(user)
                status = 'checked'
                if reversed_status == 'checked':  # remove if user set both like & unlike
                    getattr(target, reversed_choice).remove(user)
                    reversed_status = 'unchecked'

            target.save()

            data = {
                'id': request.POST.get('id'),
                'status': status,
                'target': str(target),
                'cnt': getattr(target, choice).count(),
                'reversed_status': reversed_status,
                'reversed_cnt': getattr(target, reversed_choice).count(),
            }

            return JsonResponse(data, safe=False)


@login_required
def ask_ai(request, q_id):
    print('try to run task')
    celery_task = ask_ai_task.delay(q_id)
    return redirect(reverse_lazy('question_detail', kwargs={'pk': q_id}))
