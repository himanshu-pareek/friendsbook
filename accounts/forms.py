from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import UserProfile

class RegistrationForm (UserCreationForm):
    email = forms.EmailField (required = True)
    country_list = ('Mexico', 'USA', 'China', 'France')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


        # model = UserProfile
        # fields = [
        #     'gender',
        #     'phone',
        #     'city',
        # ]
        # GENDER_CHOICES = (
        #     (0 , 'Male'),
        #     (1 , 'Female'),
        #     (2 , 'other'),
        #     (3 , 'Rather not say'),
        # )
        # widgets = {
        #     'gender': forms.RadioSelect(choices=GENDER_CHOICES),
        #     }

    def save (self, commit = True):
        user = super (RegistrationForm, self).save (commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save ()

        return user

class EditProfileForm (forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'description',
            'city',
            'website',
            'phone',
            'gender',
        )


        GENDER_CHOICES = (
            (0 , 'Male'),
            (1 , 'Female'),
            (2 , 'other'),
            (3 , 'Rather not say'),
        )

        widgets = {
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
        }
