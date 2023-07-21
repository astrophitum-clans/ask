from datetime import datetime, timedelta

from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin

from ask.models import Question


def get_random_question(user):
    """Return a random question where the author is not the current user and he`s not been asked this question before"""
    return Question.objects.exclude(author=user).exclude(answers__author=user).order_by('?').first()

    # ToDo: Optimize this method


class LastAnswerCheckMixin:
    """
    Mixin: redirect to an answer if current user`s last answer was earlier LAST_ANSWER_TIMEDELTA
    If new user - don`t redirect
    """

    # ToDo: add next to redirect

    def get(self, request, *args, **kwargs):

        LAST_ANSWER_TIMEDELTA = 24  # hours

        if request.user.is_authenticated and (
                not request.user.last_answer  # is None - first time show it
                or datetime.now() - request.user.last_answer.replace(tzinfo=None) > timedelta(
            hours=LAST_ANSWER_TIMEDELTA)
        ):
            if Question.objects.exclude(author=request.user).exclude(answers__author=request.user).exists():
                random_question = get_random_question(request.user)
                return redirect(reverse_lazy('answer_to_question', kwargs={'pk': random_question.id}))

        return super().get(request, *args, **kwargs)


class NewAnswersSumMixin(ContextMixin):
    """
    A mixin class that adds sum of new answers to all the views that use it.
    """

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            ctx['new_answers_sum'] = Question.objects.filter(author=user).aggregate(
                total=Sum('new_answers_count'))['total']
        else:
            ctx['new_answers_sum'] = None
        return ctx
