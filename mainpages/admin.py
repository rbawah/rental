from django.contrib import admin
from mainpages.models import Building, Home, HomeType, LocationProvince, LocationCity, Unit, HomePhotos

class HomePhotosAdmin(admin.StackedInline):
    model = HomePhotos

# Register your models here
class BuildingAdmin(admin.ModelAdmin):
    #list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class UnitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    inlines = [HomePhotosAdmin]
    extra = 0
 
    class Meta:
       model = Unit
    
class HomeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [HomePhotosAdmin]
    extra = 0
 
    class Meta:
       model = Home    

class HomeTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
class LocationProvinceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('province',)}
class LocationCityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('city',)}


admin.site.register(Home, HomeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(HomeType, HomeTypeAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(LocationProvince, LocationProvinceAdmin)
admin.site.register(LocationCity, LocationCityAdmin)