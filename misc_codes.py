@login_required
@permission_required('mainpages.add_home')
def home_create(request):
 
    ImageFormSet = modelformset_factory(HomePhotos, form=ImageForm, extra=3, max_num=6,)
    if request.method == 'POST':
        homeForm = HomeForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=HomePhotos.objects.none())
    
        if homeForm.is_valid() and formset.is_valid():
            home_form = homeForm.save(commit=False)
            home_form.manager = request.user
            home_form.save()
            formset.save()
    
            for form in formset.cleaned_data:
                if form:
                    pictures = form['pictures']
                    photos = HomePhotos(home=home_form, pictures=pictures)
                    photos.save()
            messages.success(request, "Successfully uploaded!")
            return HttpResponseRedirect("/allhomes/")
        else:
            print(homeForm.errors, formset.errors)
    else:
        homeForm = HomeForm()
        formset = ImageFormSet(queryset=HomePhotos.objects.none())


    return render(request, 'create_home.html', {'homeForm': homeForm, 'formset': formset})




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



            home_list = Home.objects.filter(Q(name__icontains=query) |
                                            Q(description__icontains=query) |
                                            Q(location__city__icontains=query),
                                            ).order_by('date_added')


