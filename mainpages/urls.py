from django.urls import path, reverse_lazy
from django.conf.urls import url
from mainpages.models import Building, Unit, Home
from mainpages import views
from mainpages.views import HomePageView, DashboardView, BuildingListView, UnitsListView, CityHomesView, HomeCreateView
from mainpages.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


urlpatterns = [

    path('', views.HomePageView.as_view(), name='home'),
    path('homes/<slug:slug>/', views.home_detail, name='home-detail'),
    path('dashboard/', views.DashboardView.as_view(), name = 'dashboard'),
    path('buildings/', views.BuildingListView.as_view(), name='building-list'),
    path('<slug:slug>/units/', views.UnitsListView.as_view(), name='building-units-list'), #Units in a specific building
    path('<slug:slug>/homes/', views.CityHomesView.as_view(), name='city_homes'),
    path('homes/', views.HomeSearchView.as_view(), name='home_search'),
    path('allunits/', OwnerListView.as_view(
            model = Unit,
            template_name = "allunit_list.html",
    ), name = 'allunits'),

    path('allhomes/', OwnerListView.as_view(
            model = Home,
            template_name = "allhome_list.html",
    ), name = 'allhomes'),



    path('building/create',
        OwnerCreateView.as_view(
            success_url=reverse_lazy('building-list'),
            model = Building,
            template_name = "form.html",
            permission_required = 'mainpages.add_building',
            fields = ['name',]
         ), name='building-create'),

    path('building/<slug:slug>/update',
        OwnerUpdateView.as_view(
            success_url=reverse_lazy('building-list'),
            model = Building,
            fields = ['name',],
            template_name = "form.html"
        ), name='building-update'),

    path('building/<slug:slug>/delete',
        OwnerDeleteView.as_view(
            success_url=reverse_lazy('building-list'),
            model = Building,
            template_name ="delete.html"
        ), name='building-delete'),

    path('unit/create',
        OwnerCreateView.as_view(
            success_url=reverse_lazy('allunits'),
            model = Unit,
            template_name = "form.html",
            permission_required = 'mainpages.add_unit',
            fields = ['name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'building', 'tenant', 'date_available', 'status', 'advertise',]
         ), name='unit-create'),

        path('unit/<slug:slug>/update',
        OwnerUpdateView.as_view(
            success_url=reverse_lazy('allunits'),
            model = Unit,
            fields = ['name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'building', 'tenant', 'date_available', 'status', 'advertise', ],
            template_name = "form.html"),
            name='unit-update'),

    path('unit/<slug:slug>/delete',
        OwnerDeleteView.as_view(
            success_url=reverse_lazy('allunits'),
            model = Unit,
            template_name ="delete_home.html"
        ), name='unit-delete'),


        path('housing/create', HomeCreateView.as_view(), name='home-create'),
        path('home/<slug:slug>/update', views.HomeUpdateView.as_view(), name='home-update'),


        

    path('home/<slug:slug>/delete',
        OwnerDeleteView.as_view(
            success_url=reverse_lazy('allhomes'),
            model = Home,
            template_name ="delete_home.html"
        ), name='home-delete'),

    path('tenantinfo/<slug:slug>/',
         OwnerDetailView.as_view(
             model= Home,
             template_name= "tenant_profile.html"),
         name='tenant-info'),

    ]


    