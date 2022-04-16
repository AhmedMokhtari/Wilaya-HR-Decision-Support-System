from django.shortcuts import render


# Create your views here.
def consultation(request):
    return render(request,'GestionPersonnel/consultation.html')
