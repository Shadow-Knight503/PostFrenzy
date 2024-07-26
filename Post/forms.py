import requests
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Post, Comment
from cloudinary.forms import CloudinaryFileField


def data(request):
    username = request.user.username
    return username


# INP = '''peer rounded-t bg-slate-700 h-7 min-w-[30vw]
#     placeholder-transparent focus:outline-none border-b-2 text-slate-200
#     border-blue-500 p-2 valid:border-green-600 invalid:border-red-500
#     transition-all'''
INP = ("peer rounded-t bg-slate-700 h-7 min-w-[30vw] placeholder-transparent focus:outline-none border-b-2 "
        "text-slate-200 border-blue-500 p-2 valid:border-green-600 invalid:border-red-500 transition-all")

INPF = ("rounded-t bg-slate-700 h-32 min-w-[30vw] placeholder-transparent focus:outline-none border-2 mt-4"
        "text-slate-200 border-blue-500 p-2 valid:border-green-600 invalid:border-red-500 transition-all")


class CreateUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'This is your Display name'
        }

    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = INP
        self.fields['password1'].widget.attrs['class'] = INP
        self.fields['password2'].widget.attrs['class'] = INP


class UserProfilePage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Profile_pic']
        help_texts = {}

    def __init__(self, *args, **kwargs):
        super(UserProfilePage, self).__init__(*args, **kwargs)

        self.fields['Profile_pic'].widget.attrs['onchange'] = 'profile(event)'
        self.fields['Profile_pic'].widget.attrs['class'] = INP

    Profile_pic = CloudinaryFileField(
        options={
            'folder': 'Profile/',
            'overwrite': True,
            'resource_type': 'image',
            'invalidate': True,
        })


class VerifyUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']

    def __init__(self, *args, **kwargs):
        super(VerifyUser, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = INP
        self.fields['password1'].widget.attrs['class'] = INP
        self.fields['password2'].widget.attrs['class'] = "hidden"

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None


class PstForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['Title', 'Descrp', 'Img']

    def __init__(self, *args, **kwargs):
        super(PstForm, self).__init__(*args, **kwargs)

        self.fields['Title'].widget.attrs['class'] = INP
        self.fields['Descrp'].widget.attrs['class'] = INP
        self.fields['Img'].widget.attrs['class'] = "Lolz"


class CmntForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CmntForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs['class'] = INPF

