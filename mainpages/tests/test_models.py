from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify
from mainpages import views
from mainpages.models import Home, Unit, Building, LocationProvince, LocationCity


class LocationsModelsTests(TestCase): # Testing City and Province Models

    def setUp(self):
        self.province = LocationProvince.objects.create(province='XY', slug=slugify('XY'))
        self.location = LocationCity.objects.create(city='My City', slug=slugify('My City'), province=self.province)

    def test_locations(self):
        self.assertEqual(f'{self.province.province}', 'XY')
        self.assertEqual(f'{self.province.slug}', 'xy')
        self.assertEqual(f'{self.location.city}', 'My City')        
        self.assertEqual(f'{self.location.slug}', 'my-city') 
        self.assertEqual(f'{self.location.province}', 'XY')


class HomeModelTests(TestCase):

    def setUp(self):
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

    def test_home_listing(self):
        self.assertEqual(f'{self.home}', 'Uhuh a house')
        self.assertEqual(f'{self.home.slug}', 'uhuh-a-house')
        self.assertEqual(f'{self.home.description}', 'Beautiful house')
        self.assertEqual(f'{self.home.location}', 'MyCity')
        self.assertEqual(f'{self.home.province}', 'MP')
        self.assertEqual(f'{self.home.postal_code}', 'A2B 3C4')
        self.assertEqual(f'{self.home.size}', '1258')
        self.assertEqual(f'{self.home.livingrooms}', '2')
        self.assertEqual(f'{self.home.bedrooms}', '4')
        self.assertEqual(f'{self.home.dens}', '1')
        self.assertEqual(f'{self.home.bathrooms}', '2')
        self.assertEqual(f'{self.home.status}', 'Ready')
        self.assertEqual(f'{self.home.advertise}', 'True')
        self.assertEqual(f'{self.home.location.slug}', 'mycity')
        max_length = self.home._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
        max_length = self.home._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)
        field_label = self.home._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        field_label = self.home._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')        
       

class BuildingModelTests(TestCase):

    def setUp(self):
        self.building = Building.objects.create(name='My Building 1')
        self.building.slug=slugify(self.building.name)

    def test_building_info(self):
        self.assertEqual(f'{self.building}', 'My Building 1')
        self.assertEqual(f'{self.building.slug}', 'my-building-1')


class UnitModelTests(TestCase):

    def setUp(self):
        self.province = LocationProvince.objects.create(province='MP')
        self.location = LocationCity.objects.create(city='MyCity', slug=slugify('MyCity'), province=self.province)
        self.building = Building.objects.create(name='Alburuj')
        self.building.slug=slugify(self.building.name)
        self.unit = Unit.objects.create(
            name='Exotic Condo',
            slug=slugify('exotic-condo'),
            description='Nice Condo',
            location=self.location,
            province=self.province,
            postal_code='A2B 3C4',
            size='1111',
            livingrooms='2',
            bedrooms='4',
            dens='1',
            bathrooms='2',
            status='Ready',
            advertise='True',
            building=self.building
            )

    def test_home_listing(self):
        self.assertEqual(f'{self.unit}', 'Exotic Condo')
        self.assertEqual(f'{self.unit.slug}', 'exotic-condo')
        self.assertEqual(f'{self.unit.description}', 'Nice Condo')
        self.assertEqual(f'{self.unit.location}', 'MyCity')
        self.assertEqual(f'{self.unit.province}', 'MP')
        self.assertEqual(f'{self.unit.postal_code}', 'A2B 3C4')
        self.assertEqual(f'{self.unit.size}', '1111')
        self.assertEqual(f'{self.unit.livingrooms}', '2')
        self.assertEqual(f'{self.unit.bedrooms}', '4')
        self.assertEqual(f'{self.unit.dens}', '1')
        self.assertEqual(f'{self.unit.bathrooms}', '2')
        self.assertEqual(f'{self.unit.status}', 'Ready')
        self.assertEqual(f'{self.unit.advertise}', 'True')
        self.assertEqual(f'{self.unit.location.slug}', 'mycity')
        self.assertEqual(f'{self.unit.building}', 'Alburuj')        
        max_length = self.unit._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
        max_length = self.unit._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)
        field_label = self.unit._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        field_label = self.unit._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

