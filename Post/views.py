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

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

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
    posts = Post.objects.all().order_by('-date_created')
    cmnts = Comment.objects.all()
    cmtf = CmntForm()
    pstf = PstForm()
    print(request.method, is_ajax(request), request.POST.get('Act'))
    if request.method == 'POST' and is_ajax(request) and request.POST.get('Act') == "Comment":
        print("Comment ?")
        print(request.POST.get('Act'), request.POST.get('Cmt'))
        if len(request.POST.get('Cmt')) > 0:
            cmt = Comment()
            post = Post.objects.get(id=request.POST.get('ID'))
            cmt.not_post_method_ok = post
            cmt.op = request.user
            cmt.comment = request.POST.get('Cmt')
            cmt.save()
            print("Comment Saved")
    elif request.method == 'POST':
        pstf = PstForm(request.POST, request.FILES)
        print(pstf.is_valid(), pstf.errors)
        if pstf.is_valid():
            pstf.save(commit=False)
            pstf.op = request.user
            pstf.save()
            print("Post Added")
    ctx = {
        'cmtf': cmtf,
        'pstf': PstForm,
        'posts': posts,
        'cmnts': cmnts,
        'user': data(request)[1],
        'acc': request.user,
    }
    return render(request, "Home.html", ctx)