from django import forms
from django.contrib.gis import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from salesleads.models import (

    ContactPerson,
    Country,
    Comment,
    ExportUser,
    PlannedActivities,
    SalesLead,
)

USERLIST = [(0, '-----')]
number = 1
for user in ExportUser.objects.all():
    USERLIST.append((user.id, user))
    number += 1
USERTUPPLE_without = tuple(USERLIST)
USERLIST.append((number + 1, 'Wszyscy'))

USERTUPPLE = tuple(USERLIST)


class ExportUserCreationForm(UserCreationForm):
    class Meta:
        model = ExportUser
        fields = '__all__'


class ChangeUserForm(forms.Form):
    user = forms.ChoiceField(choices=USERTUPPLE_without, label='Użytkownik')


class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')

    def clean_username(self):
        username = self.cleaned_data['username']
        if ExportUser.objects.filter(username=username).exists():
            return username
        else:
            raise ValidationError("Podany użytkownik nie istnieje!")


class SalesLeadAddForm(forms.ModelForm):
    class Meta:
        model = SalesLead
        fields = ['company_name', 'type', 'status', 'company_website', 'source', 'brands', 'potential', 'score']


class SalesLeadAddressAddForm(forms.ModelForm):
    class Meta:
        model = SalesLead
        fields = ['street', 'city', 'postcode', 'country', 'longtitude', 'latitude']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['first_name', 'last_name', 'position', 'email', 'telephone', 'whatsapp', 'linkedin_added', 'default']


class PlannedActivitiesAddForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = PlannedActivities
        fields = ['date', 'activity_type', 'activity_comment']


class PlannedActivitiesUpdateForm(forms.ModelForm):
    class Meta:
        model = PlannedActivities
        fields = ['date', 'activity_type', 'activity_comment', 'activity_done']


class MyGeoForm(forms.Form):
    point = forms.PointField(widget=
                             forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class ReportForm(forms.Form):
    initial_date = forms.DateField(label='Data początkowa', required=False)
    end_date = forms.DateField(label='Data końcowa', required=False)
    user = forms.ChoiceField(label='Użytkownik', choices=USERTUPPLE, required=False)
