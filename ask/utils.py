from datetime import datetime, timedelta

from django.shortcuts import redirect
from django.urls import reverse_lazy

from ask.models import Question


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