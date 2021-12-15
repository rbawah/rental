from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.postgres.search import  SearchQuery, SearchRank, SearchVector
from mainpages.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from mainpages.models import Building, Unit, Home, HomeType, LocationCity, HomePhotos
from mainpages.forms import ImageFormSet#, HomeForm, ImageForm, 



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
    permission_required = ('mainpages.view_building',)
    template_name = "buildings_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(name__icontains=strval)
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


class CityHomesView(ListView):
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


class HomeSearchView(ListView): #includes all homes view logic
    template_name='units_list.html'

    def get(self, request):
        strval =  request.GET.get("search", False)
        if strval :
            #query = strval
            vector = SearchVector('location__city', 'neighbourhood', 'name', 'tags', 'description', )
            query = SearchQuery(strval)
            home_list = Home.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        else :
            home_list = Home.objects.all().filter(status='Ready').order_by('date_added')
        paginator = Paginator(home_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        ctx = {'page_obj': page_obj, 'search': strval}
        return render(request, self.template_name, ctx)


def home_detail(request, slug):
    home = get_object_or_404(Home, slug=slug)
    photos = HomePhotos.objects.filter(home__slug=slug)
    ctx = {'home':home, 'photos':photos}
    return render(request, 'home_detail22.html', ctx)


class HomeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Home
    permission_required = 'mainpages.add_home',
    success_url=reverse_lazy('allhomes')
    template_name = 'create_home.html'
    fields = ('name', 'hometype', 'province', 'location', 'postal_code', 'address', 'neighbourhood', 'rent', 'size', 'livingrooms',
            'bedrooms', 'bathrooms', 'dens', 'description', 'tenant', 'date_available', 'status', 'advertise', 'tags', )

    def get_context_data(self, **kwargs):
        context = super(HomeCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['image_formset']
        object = form.save(commit=False)
        object.manager = self.request.user
        object.save()
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class HomeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Home
    permission_required = 'mainpages.change_home',
    success_url=reverse_lazy('allhomes')
    template_name = 'create_home.html'
    fields = ('name', 'hometype', 'province', 'location', 'postal_code', 'address', 'neighbourhood', 'rent', 'size', 'livingrooms',
            'bedrooms', 'bathrooms', 'dens', 'description', 'tenant', 'date_available', 'status', 'advertise', 'tags', )

    def get_context_data(self, **kwargs):
        context = super(HomeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['image_formset'].full_clean()
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['image_formset']
        object = form.save(commit=False)
        object.manager = self.request.user
        object.save()
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)