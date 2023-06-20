from django.urls import path

from .views import HomePageView, QuestionListView, MyQuestionListView, QuestionDetailView, QuestionCreateView, \
    AnswerToQuestionView, AnswerListView, AnswerToMyQuestionListView, FaqPageView, like

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('faq/', FaqPageView.as_view(), name='faq'),
    path('questions/<int:pk>/answer/', AnswerToQuestionView.as_view(), name='answer_to_question'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/create/', QuestionCreateView.as_view(), name='question_create'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/my/', MyQuestionListView.as_view(), name='my_question_list'),
    path('answers/', AnswerListView.as_view(), name='answer_list'),
    path('answers/to_my_questions/', AnswerToMyQuestionListView.as_view(), name='answer_to_my_question_list'),
    path('like/', like, name='like'),
]
