from django.urls import path

from .views import HomePageView, QuestionListView, QuestionDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('questions/', QuestionListView.as_view(), name='question_list'),

]
