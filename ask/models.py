from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Question(models.Model):
    """Base question Model"""
    text = models.TextField(max_length=1000, verbose_name=_('question'))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='questions', verbose_name=_('author'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_('is_active'))
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name=_('is_deleted'))
    like = models.ManyToManyField(get_user_model(), related_name='question_likes', verbose_name=_('likes'))
    unlike = models.ManyToManyField(get_user_model(), related_name='question_unlikes', verbose_name=_('unlikes'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Base answer model"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name=_('question'))
    text = models.TextField(max_length=1000, verbose_name=_('answer'))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('author'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_('is_active'))
    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name=_('is_deleted'))
    like = models.ManyToManyField(get_user_model(), related_name='answer_likes', verbose_name=_('like'))
    unlike = models.ManyToManyField(get_user_model(), related_name='answer_unlikes', verbose_name=_('unlike'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __str__(self):
        return self.text
