from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import FileExtensionValidator
import main.models

from main.models import goal, UserGoal, task, UserTask

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
   """Signup form fields for register.html"""
   first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
   last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
   email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
   password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
   password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
   class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )

class ChPasswordForm(PasswordChangeForm):
    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Current Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2', )


class AssignGoalForm(forms.ModelForm):

    #goal = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Your League'}),max_length=200, required=True, help_text='')
    

    class Meta:
        exclude = ('goal', 'start_date', 'goal_complete', 'owner',)
        model = UserGoal
        fields = []


class RemoveGoalForm(forms.ModelForm):
    class Meta:
        exclude = ('goal', 'start_date', 'goal_complete', 'owner',)
        model = UserGoal
        fields = []

class EditTaskForm(forms.ModelForm):
    class Meta:
        exclude = ('task', 'is_completed','owner',)
        model = UserTask
        fields = []

#<input type="hidden" type="text" value="{{goal.id}}" />
#<input type="submit" value="Assign" class="btn btn-primary" /><b> {{goal}} </b>