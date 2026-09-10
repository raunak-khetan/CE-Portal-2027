from django import forms
from django.core.validators import RegexValidator
from django.forms import modelformset_factory

from .models import Head, Team, TeamMember, YEAR_CHOICES, CFARegistration


phone_validator = RegexValidator(
    regex=r'^(?:\+91[\s-]?)?[6-9]\d{9}$',
    message='Enter a valid 10-digit mobile number.'
)


# Registration form

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Head
        fields = [
            'name',
            'gender',
            'phone_no',
            'email',
            'program_enrolled',
            'institute_name',
            'year_of_passing',
            'is_disabled'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'gender': forms.RadioSelect(),
            'phone_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 |'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'program_enrolled': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course enrolled'
            }),
            'institute_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter institute name'
            }),
            'year_of_passing': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_disabled': forms.RadioSelect(),
        }

        labels = {
            'name': "Member's Name",
            'phone_no': "Member's Contact Number",
            'email': 'E-Mail',
            'gender': 'Gender',
            'institute_name': 'Institute Name',
            'year_of_passing': 'Year of Passing',
            'program_enrolled': 'Program Enrolled',
            'is_disabled': 'Are you a person with disability (PwD)?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].choices = [
            choice
            for choice in self.fields['gender'].choices
            if choice[0] != ''
        ]

        self.fields['year_of_passing'].widget = forms.RadioSelect()
        self.fields['year_of_passing'].choices = YEAR_CHOICES

    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')

        if phone:
            phone = phone.strip()
            phone_validator(phone)

        return phone


# Team name

class TeamName(forms.ModelForm):
    class Meta:
        model = Team

        fields = ['team_name']

        widgets = {
            'team_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team name'
            }),
        }

        labels = {
            'team_name': 'Team Name',
        }


# Team member form

class MemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember

        fields = [
            'name',
            'phone_no',
            'email',
            'program_enrolled',
            'gender',
            'institute_name',
            'year_of_passing',
            'is_disabled'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter member name'
            }),
            'phone_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 |'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'program_enrolled': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
            'gender': forms.RadioSelect(),
            'institute_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter institute name'
            }),
            'year_of_passing': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_disabled': forms.RadioSelect(),
        }

        labels = {
            'name': "Member's Name",
            'phone_no': "Member's Contact Number",
            'email': 'E-Mail',
            'gender': 'Gender',
            'institute_name': 'Institute Name',
            'year_of_passing': 'Year of Passing',
            'program_enrolled': 'Program Enrolled',
            'is_disabled': 'Is this member a person with disability (PwD)?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].choices = [
            choice
            for choice in self.fields['gender'].choices
            if choice[0] != ''
        ]

        self.fields['year_of_passing'].widget = forms.RadioSelect()
        self.fields['year_of_passing'].choices = YEAR_CHOICES

    def clean_phone_no(self):
        phone = self.cleaned_data.get('phone_no')

        if phone:
            phone = phone.strip()
            phone_validator(phone)

        return phone


# CFA

class CFARegistrationStep1Form(forms.ModelForm):
    class Meta:
        model = CFARegistration
        fields = ['full_name', 'email', 'age', 'college_id_card_link', 'phone_number', 'alternate_phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Enter your age'}),
            'college_id_card_link': forms.URLInput(attrs={'placeholder': 'Enter your drive link'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'alternate_phone': forms.TextInput(attrs={'placeholder': 'Enter your alternate phone number'}),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'age': 'Age',
            'college_id_card_link': 'College ID(Google drive link)',
            'phone_number': 'Phone number',
            'alternate_phone': 'Alternate phone number(optional)',
        }