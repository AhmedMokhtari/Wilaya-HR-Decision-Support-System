from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request,'Accueil/index.html')

def connexion(request):
  return render(request,'Accueil/connexion.html')