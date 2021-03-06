from django.urls import path
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from api import views
from api.views import ( 
                        HomeListAPIView, 
                        UnitListAPIView, 
                        HomeDetailApiView,
                        )
from mainpages.models import Building, Unit, Home, HomeType, LocationCity
from api.serializers import HomeSerializer, BuildingSerializer, UnitSerializer


urlpatterns = [

    path('', views.api_root),
    path('units-generic/', UnitListAPIView.as_view(), name='unit_list'),
    path('homes-generic/', HomeListAPIView.as_view(), name='home_listgeneric'),
    path('homes-generic/<int:pk>/', HomeDetailApiView.as_view(), name='homedetail_listgeneric'),

    path('homes-api/', views.HomeListAPI.as_view(), name='home_list'),
    path('homes-api/<int:pk>/', views.HomeDetailAPI.as_view(), name='home_detail'),
    path('units-api/', views.UnitListAPI.as_view(), name='unit_list'),
    path('units-api/<int:pk>/', views.UnitDetailAPI.as_view(), name='unit_detail'),
    path('buildings-api/', views.BuildingListAPI.as_view(), name='building_list'),
    path('buildings-api/<int:pk>/', views.BuildingDetailAPI.as_view(), name='building_detail'),
    #path('<slug:slug>/units', UnitsInBuildingAPIView.as_view(), name='building_units'), #Units in a specific building
    path('building-api/create/', 
        CreateAPIView.as_view(
            serializer_class=BuildingSerializer,
            permission_classes=[IsAuthenticated]), 
            name='building_create'),

    path('home-api/create/', 
        CreateAPIView.as_view(
            serializer_class=HomeSerializer,
            permission_classes=[IsAuthenticated]), 
            name='home_create'),

    path('unit-api/create/', 
        CreateAPIView.as_view(
            serializer_class=UnitSerializer,
            permission_classes=[IsAuthenticated]), 
            name='unit_create'),

    path('users-api/', views.UserListAPI.as_view(), name='user_list'),
    path('users-api/<int:pk>/', views.UserDetailAPI.as_view()),
    ]

    