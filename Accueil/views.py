from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
      return redirect('index')
    else:
      messages.success(request,('معلومات خاطئة'))
      return redirect('connexion')
  else:
    return render(request, 'Accueil/connexion.html')
