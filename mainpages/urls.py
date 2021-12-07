from django.urls import path, reverse_lazy
from django.conf.urls import url
from mainpages.models import Building, Unit, Home
from mainpages.views import HomePageView, DashboardView, BuildingListView, UnitsListView, HomeSearchView, CityHomesView
from mainpages.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('<slug:slug>/units/', UnitsListView.as_view(), name='building-units-list'), #Units in a specific building
    path('<slug:slug>/homes/', CityHomesView.as_view(), name='city_homes'),
    #path('units/', HomeSearchView.as_view(), name='home_search'),
    path('allunits/', OwnerListView.as_view(
            model = Unit,
            template_name = "allunit_list.html",
    ), name = 'allunits'),

    path('allhomes/', OwnerListView.as_view(
            model = Home,
            template_name = "allhome_list.html",
    ), name = 'allhomes'),

    path('unit/<slug:slug>/',
         OwnerDetailView.as_view(
             model= Unit,
             template_name= "detail.html"),
         name='home-detail'),

    path('homes/<slug:slug>/',
         OwnerDetailView.as_view(
             model= Home,
             template_name= "home_detail.html"),
         name='home-detail'),

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
                 'bedrooms', 'bathrooms', 'dens', 'description', 'building', 'tenant', 'date_available', 'status', 'advertise', 'pictures',]
         ), name='unit-create'),

        path('unit/<slug:slug>/update',
        OwnerUpdateView.as_view(
            success_url=reverse_lazy('allunits'),
            model = Unit,
            fields = ['name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'building', 'tenant', 'date_available', 'status', 'advertise', 'pictures',],
            template_name = "form.html"),
            name='unit-update'),

    path('unit/<slug:slug>/delete',
        OwnerDeleteView.as_view(
            success_url=reverse_lazy('allunits'),
            model = Unit,
            template_name ="delete.html"
        ), name='unit-delete'),

        path('home/create',
        OwnerCreateView.as_view(
            success_url=reverse_lazy('allhomes'),
            model = Home,
            template_name = "form.html",
            permission_required = 'mainpages.add_home',
            fields = ['name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'tenant', 'date_available', 'status', 'advertise', 'pictures',]
         ), name='home-create'),

        path('home/<slug:slug>/update',
        OwnerUpdateView.as_view(
            success_url=reverse_lazy('allhomes'),
            model = Home,
            template_name = "form.html",
            fields = ['name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'tenant', 'date_available', 'status', 'advertise', 'pictures',]
         ), name='home-update'),         

    path('home/<slug:slug>/delete',
        OwnerDeleteView.as_view(
            success_url=reverse_lazy('allhomes'),
            model = Home,
            template_name ="delete.html"
        ), name='home-delete'),

    path('tenantinfo/<slug:slug>/',
         OwnerDetailView.as_view(
             model= Home,
             template_name= "tenant_profile.html"),
         name='tenant-info'),



    ]