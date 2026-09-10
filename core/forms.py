from django import forms
from .models import Head, Team, TeamMember, YEAR_CHOICES
from django.forms import modelformset_factory
from .models import CFARegistration


# Using YEAR_CHOICES from models to keep a single source of truth

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Head
        fields = ['name', 'gender', 'phone_no', 'email', 'program_enrolled', 'institute_name', 'year_of_passing', 'is_disabled']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'program_enrolled' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program Enrolled'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institute Name'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),  # radio → no placeholder
            'is_disabled': forms.RadioSelect(attrs={}),
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
        # Ensure there is no blank placeholder like "---------" in radios
        self.fields['gender'].choices = [choice for choice in self.fields['gender'].choices if choice[0] != '']
        # Render graduating year as radios using static choices
        self.fields['year_of_passing'].widget = forms.RadioSelect()
        self.fields['year_of_passing'].choices = YEAR_CHOICES

class TeamName(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']

        widgets = {
            'team_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Team Name'
            }),
        }
        
        labels = {
            'team_name' : 'Team Name',
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'phone_no', 'email', 'program_enrolled', 'gender', 'institute_name', 'year_of_passing', 'is_disabled']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'program_enrolled' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program Enrolled'}),
            'gender': forms.RadioSelect(attrs={'class': 'gender-option'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Institute Name'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),  # radio → no placeholder
            'is_disabled': forms.RadioSelect(attrs={}),
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
        # Ensure consistent class and remove any blank placeholder choice
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].choices = [choice for choice in self.fields['gender'].choices if choice[0] != '']
        # Render graduating year as radios using static choices
        self.fields['year_of_passing'].widget = forms.RadioSelect()
        self.fields['year_of_passing'].choices = YEAR_CHOICES


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