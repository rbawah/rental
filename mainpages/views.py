from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from mainpages.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from mainpages.models import Building, Unit, Home, HomeType, LocationCity
from django.db.models import Q


def is_manager(self):
    return self.groups.filter(name='Managers').exists

def is_tenant(self):
    return self.groups.filter(name='Tenants').exists


class HomePageView(TemplateView):
    template_name = 'home.html'

    
class DashboardView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser:
            self.template_name = 'dashboard.html'
        else:
            self.template_name = 'dashboard22.html'
        return self.template_name


class BuildingListView(OwnerListView): # Tests to be written
    #permission_required = ('building.manager_status',)
    template_name = "buildings_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(name__icontains=strval)
            #query.add(Q(description__icontains=strval), Q.OR)
            building_list = Building.objects.filter(query).order_by('name')
        else :
            building_list = Building.objects.all().order_by('name')
        paginator = Paginator(building_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ctx = {'page_obj': page_obj, 'search': strval}
        return render(request, self.template_name, ctx)


class UnitsListView(OwnerListView):
    template_name = 'units_list.html'

    def get(self, request, slug):
        building = Building.objects.get(slug=slug)
        units_list = Unit.objects.filter(
            building__name=building
        )

        paginator = Paginator(units_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ctx = {'page_obj': page_obj, 'units_list': units_list, 'building':building}
        return render(request, self.template_name, ctx)


class CityHomesView(OwnerListView):
    template_name = 'units_list.html'

    def get(self, request, slug):
        city = LocationCity.objects.get(slug=slug)
        homes = Home.objects.filter(
            location__slug=slug, status='Ready'
        )

        paginator = Paginator(homes, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ctx = {'page_obj': page_obj, 'city': city, 'homes':homes}
        return render(request, self.template_name, ctx)


class HomeSearchView(OwnerListView):
    model = Home
    context_object_name = "home_list"
    template_name='allunit_list.html'

    def get_queryset(self):
        query = self.request.GET.get('searchpage')
        return Home.objects.filter(location__city__icontains=query)


