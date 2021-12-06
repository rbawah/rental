from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.contrib.auth import get_user_model
User = get_user_model()


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

"""
def view_tenant_profile(request, username): #Manager's view of tenants' profile
    tenant = User.objects.get(username=username) # Add UUID
    return render(request, 'tenant_profile.html', {"tenant":tenant})
"""

class UserProfileView(generic.DetailView):
    template_name = 'user_profile.html'
    model = User

    def get_object(self, queryset=None):
        user = self.request.user
        return user

"""
def edit_user(request):
    user = request.user
    #user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=(
            'first_name',
            'last_name',
            'date_of_birth',
            'city',
            'phone_number',))

    formset = ProfileInlineFormset(instance=user)
    if request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/blog/profile/')
        return render(request, "blog/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
"""
def userchange_view(request):

	if not request.user.is_authenticated:
		return redirect("login")
	ctx = {}
	if request.POST:
		form = CustomUserChangeForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
	else:
		form = CustomUserChangeForm(
				initial= {
					"email": request.user.email,
					"username": request.user.username,
				}
			)
	return render(request, 'account/account_update.html', {"form" : form})