from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from webecseg.core.forms import SignUpForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage, File
from django.http import HttpResponse
import os

@login_required
def home(request):
    if not os.path.isdir(os.path.join(settings.RESULT_ROOT,request.user.username)):
	if not os.path.isdir(settings.RESULT_ROOT):
	    os.mkdir(settings.RESULT_ROOT)
	os.mkdir(os.path.join(settings.RESULT_ROOT,request.user.username))
    if not os.path.isdir(settings.IMAGE_ROOT+'/'+request.user.username):
	if not os.path.isdir(settings.IMAGE_ROOT):
	    os.mkdir(settings.IMAGE_ROOT)
	os.mkdir(os.path.join(settings.IMAGE_ROOT,request.user.username))

    return render(request, 'home.html' )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


