from mainpages.models import LocationCity


def cities_homepage(request):
    ''' Returns necessary information for homepage
    '''
    
    cities = LocationCity.objects.all()

    return {
        'cities': cities,

    }