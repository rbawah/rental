import datetime
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
#from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import uuid
from ckeditor_uploader.fields import RichTextUploadingField


class HomeType(models.Model):
    """Model representing the type of home, eg, Apartment, Condo, House, etc."""
    name = models.CharField(max_length=25, help_text = 'Select the Home Type (e.g. Apartment, Condo, House)')
    slug = models.SlugField(null = True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'home type'
        verbose_name_plural = "home types"    
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse('hometypes', kwargs={'slug': self.slug})

class LocationProvince(models.Model):
    province = models.CharField(max_length=30,)
    slug = models.SlugField(null = True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.province)
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['province']
        verbose_name = 'province'
        verbose_name_plural = "provinces" 

    def __str__(self):
        """String for representing the Model object."""
        return self.province

    def get_absolute_url(self):
        return reverse('province-homes', kwargs={'slug': self.slug})

class LocationCity(models.Model):
    province = models.ForeignKey('LocationProvince', on_delete=models.CASCADE)
    city = models.CharField(max_length=30,)
    image = models.ImageField(upload_to='cities/', blank=True,)
    slug = models.SlugField(null = True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.city)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['city']
        verbose_name = 'city'
        verbose_name_plural = "cities" 

    def __str__(self):
        """String for representing the Model object."""
        return self.city
        #return f'{self.city}, {self.province}'

    def get_absolute_url(self):
        return reverse('city-homes', kwargs={'slug': self.slug})


class AbstractHome(models.Model):

    """Model representing a home (but not a specific instance in db)."""

    address = models.CharField(max_length=200, blank=True)
    location = models.ForeignKey('LocationCity', on_delete=models.CASCADE)
    province = models.ForeignKey('LocationProvince', on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=7, validators=[MinLengthValidator(7, 
        "Postal Code must be 7 characters.")],)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text = 'Enter a brief description of the home')
    hometype = models.ForeignKey('HomeType', on_delete=models.SET_NULL, 
        null=True, help_text='Select the Home Type (e.g. Apartment, Condo, House)',)
    size = models.IntegerField()
    livingrooms = models.IntegerField(help_text = 'Number of Living Rooms')
    bedrooms = models.IntegerField(help_text = 'Number of Bedrooms ')
    dens = models.IntegerField(help_text = 'Number of Dens')
    bathrooms = models.DecimalField(help_text = 'Number of Bathrooms', max_digits=3, decimal_places=1)
    advertise = models.BooleanField(help_text = 'Advertise this Unit?', default=False)
    tags = models.CharField(max_length=200, blank=True, help_text='Enter search tags separated by commas.')

    class Meta:
        abstract = True



class Building(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buildings_manager', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(null = False, unique = True,)

#    class Meta:


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail/units information for the building."""
        return reverse('building-units-list', args=[str(self.slug)])


class Home(AbstractHome):
    ud = models.UUIDField(default=uuid.uuid4, editable = False, help_text='Unique ID for a Home.')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name = 'homes_tenant')
    date_available = models.DateField(null=True, blank=True)    
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name = 'homes_manager')
    date_added = models.DateTimeField(default=timezone.now)
    #pictures = RichTextUploadingField(blank=True,)
    #picture = models.ImageField(blank=True,)
    slug = models.SlugField(null = False, unique = True)

    STATUS_CHOICES = [
        ('Ready', 'Ready'), #Ready to be occupied
        ('Occupied', 'Occupied'), # Has a tenant
        ('Available', 'Available'),# Empty but may not be ready for renting out.
        ('Renovation', 'Renovation'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        help_text='Availability Status',
    )


    class Meta(AbstractHome.Meta):
        verbose_name = 'Home'
        verbose_name_plural = "Homes"
        ordering = ['date_added']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail information for the home."""
        return reverse('home-detail', args=[str(self.slug)])

     
class Unit(Home):
    building = models.ForeignKey(Building, related_name='units_building', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(Home.Meta):
        verbose_name = 'Unit'
        verbose_name_plural = "Units"



class HomePhotos(models.Model):
    home = models.ForeignKey(Home, default=None, on_delete=models.CASCADE, related_name = 'pics_home',)
    pictures = models.ImageField(upload_to = 'homes/', blank = True, )
''' 
    def __str__(self):
        return self.home.name

    '''