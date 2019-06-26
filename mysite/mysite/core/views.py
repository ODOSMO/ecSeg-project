from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from mysite.core.forms import SignUpForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage, File
from django.http import HttpResponse
import os
import generate_html

@login_required
def home(request):
    if not os.path.isdir(os.path.join(settings.RESULT_ROOT,request.user.username)):
	if not os.path.isdir(settings.RESULT_ROOT):
		os.mkdir(settings.RESULT_ROOT)
	os.mkdir(os.path.join(settings.RESULT_ROOT,request.user.username))
    if not os.path.isdir(settings.QUERY_ROOT+'/'+request.user.username):
	if not os.path.isdir(settings.QUERY_ROOT):
		os.mkdir(settings.QUERY_ROOT)
	os.mkdir(os.path.join(settings.QUERY_ROOT,request.user.username))

    fs = FileSystemStorage(location=settings.QUERY_ROOT+'/'+request.user.username)
    filelist = fs.listdir(settings.QUERY_ROOT + "/" + request.user.username)
    querylist = filelist[1]
    if request.method == 'POST':
	q_path = os.path.join(settings.QUERY_ROOT,request.user.username,request.POST.get('query'))
   	boolstring = False
    	if request.POST.get('aoption') == 'True':
		boolstring = True
    	generate_html.output( request.user.username, settings.RESULT_ROOT, q_path, settings.DATABASE_ROOT, a=boolstring)

    return render(request, 'home.html' , {"filelist": querylist})


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

def query_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=settings.QUERY_ROOT+'/'+request.user.username)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'query_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'query_upload.html')

def database_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=settings.DATABASE_ROOT+'/'+request.user.username)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'database_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'database_upload.html')
def uploaded_query(request):
    fs = FileSystemStorage(location=settings.QUERY_ROOT+'/'+request.user.username)
    filelist = fs.listdir(settings.QUERY_ROOT+"/"+request.user.username)
    querylist = filelist[1]
    return render(request, 'uploaded.html', {"filelist": querylist})


def download(request, filename):
    file_path = os.path.join(settings.QUERY_ROOT, request.user.username, filename)
    with open(file_path, 'rb') as f:
        todownload = File(f)

        response = HttpResponse(todownload.chunks(), content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_path)

        return response

def user_result(request):
    fs = FileSystemStorage(location=settings.RESULT_ROOT+'/'+request.user.username)
    filelist = fs.listdir(settings.RESULT_ROOT+'/'+request.user.username)
    result_list = []
    for f in filelist[1]:
	if 'html' in f:
	    result_list.append(f)
    return render(request, 'result.html', {"resultlist":result_list})


def download_result(request, filename):
    file_path = os.path.join(settings.RESULT_ROOT, request.user.username, filename)
    with open(file_path, 'rb') as f:
        todownload = File(f)

        response = HttpResponse(todownload.chunks(), content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_path)

        return response

#def button(request):
    
    #return render(request, 'home.html')

def run_query_search(request):
    
    return render(request,'home.html')
