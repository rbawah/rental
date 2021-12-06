from django.contrib.auth.models import AbstractUser, Group
from mainpages.models import LocationCity
from django.db import models


class CustomUser(AbstractUser):
    group = models.ManyToManyField(Group)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True) # Change to django-phonenumberfield
    secondary_phone_number = models.CharField(max_length=12, null=True) # Change to django-phonenumberfield
    current_address = models.CharField(max_length=200, null=True)
    city = models.ForeignKey(LocationCity, on_delete=models.SET_NULL, null=True)

    EMP_STATUS_CHOICES = (
        ('e', 'Employed'),
        ('u', 'Unemployed'),
        ('s', 'Self-employed'),
    )
    employment_status = models.CharField(
        max_length=1,
        choices=EMP_STATUS_CHOICES,
        blank=True,
        help_text='Employment Status',
    )

    class Meta:
        
        permissions = (
            ("can_add_home", "Can Add Home"),
            )

    def is_manager(self):
        return self.groups.filter(name='Managers').exists