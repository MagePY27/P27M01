from django.views.generic import ListView

from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin


class PermListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    redirect_field_name = None

    template_name = 'permission_list.html'
    model = Permission
