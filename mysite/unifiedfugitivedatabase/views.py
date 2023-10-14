from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import viewsets
from .serializers import FugitiveProfilesSerializer
from .models import FugitiveProfiles

class FugitiveProfilesView(viewsets.ModelViewSet):
    serializer_class = FugitiveProfilesSerializer
    queryset = FugitiveProfiles.objects.all()



# Create your views here.
def search(request):
    greet = 'hello'
    context = {'greetings': greet}
    return render(request, 'search.html', context)

def database(request):
    return render(request, 'database.html')

def records(request):
    pass

def analytics(request):
    return render(request, 'analytics.html')

def map(request):
    return render(request, 'choropleth.html')

def about(request):
    return render(request, 'about.html')
