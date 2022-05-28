from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required





# Create your views here.
def index(request):
  return render(request, 'Accueil/index.html')


def connexion(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('personnel/consultation')
    else:
      messages.success(request,('معلومات خاطئة'))
      return redirect('connexion')
  else:
    return render(request, 'Accueil/connexion.html')


@login_required(login_url='/connexion')
def test(request):
    return render(request, 'Accueil/test.html')


# Create your views here.
@login_required(login_url='/connexion')
def accueil(request):
  return render(request, 'Accueil/accueil.html')