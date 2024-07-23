from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from Post.forms import UserProfilePage, CreateUser, VerifyUser, CmntForm, PstForm
from Post.models import UserProfile, Post, Comment
from django.contrib import messages


def data(request):
    username = request.user.id
    users = UserProfile.objects.get(user_id=username)
    url = users.Profile_pic.url
    name = request.user
    return url, name

def auth(request):
    profiles = UserProfilePage()
    forms = CreateUser()
    verfy = VerifyUser()
    if request.method == 'POST':
        profiles = UserProfilePage(request.POST, request.FILES)
        forms = CreateUser(request.POST)
        if forms.is_valid() and profiles.is_valid():
            user = forms.save(commit=False)
            username = forms.cleaned_data.get('username')
            user.username = username
            forms.save()
            group = Group.objects.get(name='User')
            user.groups.add(group)
            profile = profiles.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Account was successfully created for ' + username)
            return redirect('Home')
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password1')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request, "Username or Password is Incorrect")
            print("Username or Password is Incorrect")
    ctx = {
        'forms': forms,
        'verfy': verfy,
        'profiles': profiles,
    }
    return render(request, 'Login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('Login')


def home(request):
    posts = Post.objects.all()
    cmnts = Comment.objects.all()
    cmtf = CmntForm()
    if request.method == 'POST':
        print("We're In")
        cmtf = CmntForm(request.POST)
        idm = request.POST.get("ID")
        print(idm, request.POST)
        if cmtf.is_valid():
            cmt = cmtf.save(commit=False)
            post = Post.objects.get(id=idm)
            cmt.not_post_method_ok = post
            cmt.op = request.user
            cmt.comment = request.POST.get("Cmt")
            cmt.save()
            print("Done")
    ctx = {
        'cmtf': cmtf,
        'posts': posts,
        'cmnts': cmnts,
        'user': data(request)[1],
    }
    return render(request, "Home.html", ctx)