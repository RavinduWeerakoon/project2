from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Video 
import re
User = get_user_model()

from django.core.exceptions import ValidationError



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
	tube_url = forms.URLField(label="Youtube Channel Url")



class VideoForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'url'}), help_text="enter the url taken from Youtube share option")

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if 'www.youtube.com' in url:

            url =url.replace('www.youtube.com', 'youtu.be')
        if 'youtu.be' not in url:
            raise ValidationError('Your URL should be a youtube video')

        return url



class ContactForm(forms.Form):
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}))
	