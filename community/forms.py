from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Video 

User = get_user_model()


class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
            'email': None,
            'password':None,
            'password_confirmation':None,
        }


class TubeUrlForm(forms.Form):
	tube_url = forms.URLField()


class VideoForm(forms.Form):
	embed_script = forms.CharField(widget=forms.Textarea(attrs={'rows': '5',
																'placeholder':'copy paste the embed script on yt'}))
	url = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'enter the video url'}))

class ContactForm(forms.Form):
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}))
	