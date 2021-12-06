from django.contrib.auth import get_user_model
from django.urls import path
from accounts import views
#from accounts.views import SignupPageView, UserProfileView
from mainpages.models import Home
from mainpages.owner import OwnerDetailView


urlpatterns = [
    path('signup/', views.SignupPageView.as_view(), name='signup'),
    #path('profile/tenant/<username:username>', views.view_tenant_profile, name='tenant-profile'),
    path('profile/view/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', views.userchange_view, name='user_change'),

    path('tenantinfo/<slug:slug>/',
         OwnerDetailView.as_view(
             model= Home,
             template_name= "tenant_profile.html"),
         name='tenant-info'),

]

