from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify
from mainpages import views
from mainpages.models import Home, Unit, Building, LocationProvince, LocationCity


class HomepageTests(SimpleTestCase):

    databases = '__all__' # Because the homepage makes database hits to display the cities-home links(urls)

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'home.html')
        self.assertContains(self.response, 'DjangoRealtor')
        self.assertNotContains(self.response, 'Hi there! Stranger, I am leaving now.')
        view = resolve('/')
        self.assertEqual(view.func.__name__, views.HomePageView.as_view().__name__)


class DashboardTests(TestCase):

    def setUp(self):

        self.tenant = get_user_model().objects.create_user(
            username='renter1',
            email='renting@email.com',
            password='test12345'
        )

        self.manager = get_user_model().objects.create_user(
            username='manager1',
            email='managing@email.com',
            password='test12345'
        )        
        self.group = Group(name='Managers')
        self.group.save()
        self.manager.groups.add(self.group)

    def test_dashboard_view_for_tenant(self):
        self.client.login(email='renting@email.com', password='test12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tenant Profile')
        self.assertNotContains(response, 'Hi there! Stranger, I am leaving now.')
        self.assertTemplateUsed(response, 'dashboard22.html')
        #view = resolve('/dashboard/')

    def test_dashboard_view_for_manager(self):
        self.client.login(email='managing@email.com', password='test12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Portfolio')
        self.assertNotContains(response, 'Hi there! Stranger, I am leaving now.')
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_view_resolves_url(self):
        view = resolve('/dashboard/')
        self.assertEqual(view.func.__name__, views.DashboardView.as_view().__name__)

    def test_dashboard_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/dashboard/' % (reverse('account_login')))
        response = self.client.get('%s?next=/dashboard/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')        






