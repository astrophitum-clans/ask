from django.urls import path

from .views import HomePageView, QuestionListView, QuestionDetailView, QuestionCreateView, AnswerToQuestionView, \
    AnswerListView, FaqPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('faq/', FaqPageView.as_view(), name='faq'),
    path('questions/<int:pk>/answer/', AnswerToQuestionView.as_view(), name='answer_to_question'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/create/', QuestionCreateView.as_view(), name='question_create'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('answers/', AnswerListView.as_view(), name='answer_list'),

]
