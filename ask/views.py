import random
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Question, Answer
from .utils import LastAnswerCheckMixin


# Create your views here.

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


@login_required
def like(request):
    """Set/unset likes & unlikes to target"""
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id')
        choice = request.POST.get('choice')
        # reverse_choice = 'unlike' if choice == 'like' else choice
        target_model = None
        if request.POST.get('target') == 'question':
            target_model = Question
        elif request.POST.get('target') == 'answer':
            target_model = Answer

        if target_model and choice in 'like unlike'.split():
            target = get_object_or_404(target_model, pk=id)

            # # set reverse choice status
            # reverse_status = 'checked' if user in getattr(target, reverse_choice).all() else 'unchecked'

            # set choice to model & its status
            if user in getattr(target, choice).all():   # ex: question.unlike.all()
                getattr(target, choice).remove(user)
                status = 'unchecked'
            else:
                getattr(target, choice).add(user)
                status = 'checked'
                # if user in getattr(target, reverse_choice).all():   # remove if user set both like & unlike
                #     getattr(target, reverse_choice).remove(user)
                #     reverse_status = 'unchecked'

            target.save()

            data = {
                'user': request.user.username,
                'id': request.POST.get('id'),
                'status': status,
                'target': str(target),
                'cnt': getattr(target, choice).count(),
                # 'reverse_status': reverse_status,
                # 'reverse_cnt': getattr(target, reverse_choice).count(),
            }

            return JsonResponse(data, safe=False)
