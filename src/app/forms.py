from django import forms

from app.models import PlantedTree


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class PlantedTreesForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ['latitude', 'longitude', 'age', 'tree']

        widgets = {
            'latitude': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.00001'}
            ),
            'longitude': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.00001'}
            ),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'tree': forms.Select(attrs={'class': 'form-control'}),
        }
