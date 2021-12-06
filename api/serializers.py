from rest_framework import serializers
from mainpages.models import Building, Unit, Home, HomeType, LocationCity
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    buildings_manager = serializers.HyperlinkedRelatedField(many=True, view_name='building_detail', read_only=True)   
    homes_tenant = serializers.HyperlinkedRelatedField(many=True, view_name='home_detail', read_only=True)
    homes_manager = serializers.HyperlinkedRelatedField(many=True, view_name='home_detail', read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class HomeSerializer(serializers.ModelSerializer):

    manager = serializers.ReadOnlyField(source='manager.username')

    class Meta:
        model = Home
        fields = ('name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'tenant', 'date_available', 'status', 'advertise', 'manager',)


class UnitSerializer(serializers.ModelSerializer):

    manager = serializers.ReadOnlyField(source='manager.username')


    class Meta:
        model = Unit
        fields = ('name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'building', 'tenant', 'date_available', 'status', 'advertise', 'pictures', 'manager',)


class BuildingSerializer(serializers.ModelSerializer):
    manager = serializers.ReadOnlyField(source='manager.username')
    units_building = serializers.HyperlinkedRelatedField(many=True, view_name='unit_detail', read_only=True)

    class Meta:
        model = Building
        #fields = '__all__'
        fields = ('name', 'manager', 'units_building', )