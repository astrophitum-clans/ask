from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView


# Create your tests here.

class HomePageTests(SimpleTestCase):
    """Test Home page"""

    def setUp(self) -> None:
        url = reverse('home')
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        """homepage url exists"""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """homepage uses correct template"""
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        """Check if title of homepage is correct"""
        self.assertContains(self.response, 'Ask :: Home')

    def test_homepage_url_resolves_homepage_view(self):
        """Homepage url uses correct view class"""
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
