from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify
from mainpages import views
from mainpages import owner
from mainpages.models import Home, Unit, Building, LocationProvince, LocationCity


class HomeTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
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
        self.create_perm = Permission.objects.get(codename='add_home')
        self.province = LocationProvince.objects.create(province='MP')
        self.location = LocationCity.objects.create(city='MyCity', slug=slugify('MyCity'), province=self.province)

        
        self.home = Home.objects.create(
            name='Uhuh a house',
            slug=slugify('Uhuh a house'),
            description='Beautiful house',
            location=self.location,
            province=self.province,
            postal_code='A2B 3C4',
            size='1258',
            livingrooms='2',
            bedrooms='4',
            dens='1',
            bathrooms='2',
            status='Ready',
            advertise='True',
            )

    def test_cityhomes_list_view(self):
        response = self.client.get(reverse('city_homes', kwargs={'slug':self.location.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uhuh a house')
        self.assertNotContains(response, 'Hi there! Stranger, I am leaving now.')
        self.assertTemplateUsed(response, 'units_list.html')

    def test_home_owner_detail_view_for_authenticated_user(self):
        self.client.login(email='renting@email.com', password='test12345')
        response = self.client.get(reverse('home-detail', kwargs={'slug':self.home.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uhuh a house')
        self.assertNotContains(response, 'Hi there! Stranger, I am leaving now.')
        self.assertTemplateUsed(response, 'home_detail.html')       


    def test_home_owner_detail_view_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('home-detail', kwargs={'slug':self.home.slug}))
        self.assertEqual(response.status_code, 302)


class BuildingCreateViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
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
        self.create_perm = Permission.objects.get(codename='add_building')        
        self.group.permissions.add(self.create_perm)
        self.manager.groups.add(self.group)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('building-create'))        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/building/create')        
        self.assertRedirects(response, '%s?next=/building/create' % (reverse('account_login')))
        response = self.client.get('%s?next=/building/create/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_redirect_to_home_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='renting@email.com', password='test12345')
        response = self.client.get(reverse('building-create'))
        self.assertEqual(response.status_code, 302)        
        self.assertRedirects(response, '/')
        response = self.client.get('/')      
        self.assertContains(response, 'DjangoRealtor')
       

    def test_logged_in_with_permission(self):
        login = self.client.login(email='managing@email.com', password='test12345')
        response = self.client.get(reverse('building-create'))
        self.assertEqual(response.status_code, 200)        
        self.assertContains(response, 'Submit')

    def test_uses_correct_template(self):
        login = self.client.login(email='managing@email.com', password='test12345')
        response = self.client.get(reverse('building-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(email='managing@email.com', password='test12345')
        response = self.client.post(reverse('building-create'), {'name': 'Awesome Fortress'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/buildings/'))


class BuildingListViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
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
        self.create_perm = Permission.objects.get(codename='add_building')        
        self.group.permissions.add(self.create_perm)
        self.manager.groups.add(self.group)


