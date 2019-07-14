from profiles.models import Profile
import django_filters
from django import forms
from django_filters.filters import MultipleChoiceFilter, RangeFilter, NumericRangeFilter
from django_filters.widgets import RangeWidget
# Filter for bisexual users
class ProfileFilter(django_filters.FilterSet):
    hair_colour = MultipleChoiceFilter(choices=Profile.HAIR_COLOUR, label="", widget=forms.SelectMultiple(attrs={'title': 'Hair Colour ▾'}))
    body_type = MultipleChoiceFilter(choices=Profile.BODY_TYPE, label="", widget=forms.SelectMultiple(attrs={'title': 'Body Type ▾'}))
    hair_length = MultipleChoiceFilter(choices=Profile.HAIR_LENGTH, label="", widget=forms.SelectMultiple(attrs={'title': 'Hair Lenght ▾'}))
    ethnicity = MultipleChoiceFilter(choices=Profile.ETHNICITY, label="", widget=forms.SelectMultiple(attrs={'title': 'Ethnicity ▾'}))
    relationship_status = MultipleChoiceFilter(choices=Profile.RELATIONSHIP_STATUS, label="", widget=forms.SelectMultiple(attrs={'title': 'Relationship Status ▾'}))
    gender = MultipleChoiceFilter(choices=Profile.GENDER, label="", widget=forms.SelectMultiple(attrs={'title': 'Gender ▾'}))

    
    class Meta:
        model = Profile
        # add age
        fields = ['hair_colour', 'body_type', 'hair_length', 'ethnicity', 'relationship_status', 'gender' ]

# Filter not for bisexual users
class GenderlessProfileFilter(django_filters.FilterSet):
    hair_colour = MultipleChoiceFilter(choices=Profile.HAIR_COLOUR, label="", widget=forms.SelectMultiple(attrs={'title': 'Hair Colour ▾'}))
    body_type = MultipleChoiceFilter(choices=Profile.BODY_TYPE, label="", widget=forms.SelectMultiple(attrs={'title': 'Body Type ▾'}))
    hair_length = MultipleChoiceFilter(choices=Profile.HAIR_LENGTH, label="", widget=forms.SelectMultiple(attrs={'title': 'Hair Length ▾'}))
    ethnicity = MultipleChoiceFilter(choices=Profile.ETHNICITY, label="", widget=forms.SelectMultiple(attrs={'title': 'Ethnicity ▾'}))
    relationship_status = MultipleChoiceFilter(choices=Profile.RELATIONSHIP_STATUS, label="", widget=forms.SelectMultiple(attrs={'title': 'Relationship Status ▾'}))
    education = MultipleChoiceFilter(choices=Profile.EDUCATION, label="", widget=forms.SelectMultiple(attrs={'title': 'Education ▾'}))

    
    class Meta:
        model = Profile
        fields = ['hair_colour', 'body_type', 'hair_length', 'ethnicity', 'relationship_status', 'education' ]