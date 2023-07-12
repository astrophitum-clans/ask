import time

import openai
from celery import shared_task
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from ask.models import Question, Answer
from django_project import settings


@shared_task
def ask_ai_task(question_id):
    ai_user = get_object_or_404(get_user_model(), is_ai=True)
    question = get_object_or_404(Question, pk=question_id)

    openai.api_key = settings.OPENAI_KEY
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "user", "content": question.text}])
    try:
        ai_answer = chat_completion.choices[0].message.content
    except Exception as e:
        return False
    Answer.objects.create(
        question=question,
        text=ai_answer,
        author=ai_user
    )
    return True
