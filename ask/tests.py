from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, timezone

from .views import HomePageView, QuestionListView
from .models import Question, Answer


# Create your tests here.

# class HomePageTests(SimpleTestCase):
#     """Test Home page"""
#
#     def setUp(self) -> None:
#         url = reverse('home')
#         self.response = self.client.get(url)
#
#     def test_url_exists_at_correct_location(self):
#         """homepage url exists"""
#         self.assertEqual(self.response.status_code, 200)
#
#     def test_homepage_template(self):
#         """homepage uses correct template"""
#         self.assertTemplateUsed(self.response, 'home.html')
#
#     def test_homepage_contains_correct_html(self):
#         """Check if title of homepage is correct"""
#         self.assertContains(self.response, 'Ask :: Home')
#
#     def test_homepage_url_resolves_homepage_view(self):
#         """Homepage url uses correct view class"""
#         view = resolve('/')
#         self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AskTests(TestCase):
    """Test Ask application"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.testuser = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testuser123'
        )
        cls.testuser2 = get_user_model().objects.create_user(
            username='testuser2',
            email='testuser2@email.com',
            password='testuser123'
        )
        cls.questions = list()
        cls.questions.extend([
            Question.objects.create(
                text='question_1?',
                author=cls.testuser,
            ),
            Question.objects.create(
                text='question_2?',
                author=cls.testuser2,
            ),
        ])

    def test_question_list_view_for_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=/questions/" % (reverse("account_login")))
        response = self.client.get("%s?next=/questions/" % (reverse("account_login")))
        self.assertContains(response, "Log In")

    def test_question_list_view_for_login_user_if_all_questions_not_answered(self):
        self.client.login(email='testuser@email.com', password='testuser123')
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s" % (reverse("answer_to_question", kwargs={"pk": 2})))  # 2 is second question pk

    def test_question_list_view_for_login_user_if_all_questions_answered(self):
        self.client.login(email='testuser@email.com', password='testuser123')
        Answer.objects.create(
            text='testuser1 answer',
            author=self.testuser,
            question=self.questions[1],  # Answer to testuser2`s question,
        )
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "question_1?")
        self.assertTemplateUsed(response, "ask/question_list.html")

    def test_question_list_view_for_login_user_if_last_answer_not_overdue(self):
        self.client.login(email='testuser@email.com', password='testuser123')
        self.testuser.last_answer = datetime.now(timezone.utc)
        self.testuser.save()
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "question_1?")
        self.assertTemplateUsed(response, "ask/question_list.html")

    def test_question_list_view_for_login_user_if_last_answer_overdue(self):
        self.client.login(email='testuser@email.com', password='testuser123')
        self.testuser.last_answer = datetime.now(timezone.utc) - timedelta(hours=2)
        self.testuser.save()
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s" % (reverse("answer_to_question", kwargs={"pk": 2})))  # 2 is second question pk
