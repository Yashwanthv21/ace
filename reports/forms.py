from collections import OrderedDict

from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name', 'last_login', 'date_joined')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()