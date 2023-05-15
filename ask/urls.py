from django.urls import path

from .views import HomePageView, QuestionListView, QuestionDetailView, QuestionCreateView, AnswerToQuestionView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('questions/<int:pk>/answer/', AnswerToQuestionView.as_view(), name='answer_to_question'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/create/', QuestionCreateView.as_view(), name='question_create'),
    path('questions/', QuestionListView.as_view(), name='question_list'),

]
