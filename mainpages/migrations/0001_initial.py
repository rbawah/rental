# Generated by Django 3.2.10 on 2021-12-10 06:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200)),
                ('postal_code', models.CharField(max_length=7, validators=[django.core.validators.MinLengthValidator(7, 'Postal Code must be 7 characters.')])),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Enter a brief description of the home', max_length=1000)),
                ('size', models.IntegerField()),
                ('livingrooms', models.IntegerField(help_text='Number of Living Rooms')),
                ('bedrooms', models.IntegerField(help_text='Number of Bedrooms ')),
                ('dens', models.IntegerField(help_text='Number of Dens')),
                ('bathrooms', models.DecimalField(decimal_places=1, help_text='Number of Bathrooms', max_digits=3)),
                ('advertise', models.BooleanField(default=False, help_text='Advertise this Unit?')),
                ('ud', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID for a Home.')),
                ('date_available', models.DateField(blank=True, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(unique=True)),
                ('status', models.CharField(choices=[('Ready', 'Ready'), ('Occupied', 'Occupied'), ('Available', 'Available'), ('Renovation', 'Renovation')], help_text='Availability Status', max_length=10)),
            ],
            options={
                'verbose_name': 'Home',
                'verbose_name_plural': 'Homes',
                'ordering': ['date_added'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Select the Home Type (e.g. Apartment, Condo, House)', max_length=25)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'home type',
                'verbose_name_plural': 'home types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LocationProvince',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'province',
                'verbose_name_plural': 'provinces',
                'ordering': ['province'],
            },
        ),
        migrations.CreateModel(
            name='LocationCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='cities/')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpages.locationprovince')),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
                'ordering': ['city'],
            },
        ),
        migrations.CreateModel(
            name='HomePhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pictures', models.ImageField(blank=True, upload_to='homes/')),
                ('home', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pics_home', to='mainpages.home')),
            ],
        ),
        migrations.AddField(
            model_name='home',
            name='hometype',
            field=models.ForeignKey(help_text='Select the Home Type (e.g. Apartment, Condo, House)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainpages.hometype'),
        ),
        migrations.AddField(
            model_name='home',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpages.locationcity'),
        ),
        migrations.AddField(
            model_name='home',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homes_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='home',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpages.locationprovince'),
        ),
        migrations.AddField(
            model_name='home',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homes_tenant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buildings_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('home_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainpages.home')),
                ('building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='units_building', to='mainpages.building')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
                'abstract': False,
            },
            bases=('mainpages.home',),
        ),
    ]
