from django import forms
from django.forms.models import inlineformset_factory
from mainpages.models import Home, HomePhotos


ImageFormSet = inlineformset_factory(Home, HomePhotos, fields = ['pictures',],)

class HomeForm(forms.ModelForm):
 
    class Meta:
        model = Home
        fields = ('name', 'hometype', 'province', 'location', 'postal_code', 'address', 'size', 'livingrooms',
                 'bedrooms', 'bathrooms', 'dens', 'description', 'tenant', 'date_available', 'status', 'advertise', 'tags',)
 
 
class ImageForm(forms.ModelForm):
    pictures = forms.ImageField(label='Pictures')    
    class Meta:
        model = HomePhotos
        fields = ('pictures', )