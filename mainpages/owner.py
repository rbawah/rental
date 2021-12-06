
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('home')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class OwnerListView(ListView):

    """
    Sub-class the ListView to pass the request to the form.
    """


class OwnerDetailView(LoginRequiredMixin, DetailView):
    #permission_required = ('mainpages.building.manager_status', 'mainpages.home.manager_status')
    #permission_denied_message = "You are not Permitted to access this Page"
    """
    Sub-class the DetailView to pass the request to the form.
    """


class OwnerCreateView(LoginRequiredMixin, UserAccessMixin, CreateView):
    
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """
    #login_url = 'account_login'
    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        object = form.save(commit=False)
        object.manager = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    #permission_required = ('building.manager_status', 'home.manager_status')
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(manager=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    #permission_required = ('building.manager_status', 'home.manager_status')
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(manager=self.request.user)

