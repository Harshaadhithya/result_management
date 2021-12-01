from django.shortcuts import render
from .models import Profile,Department

# Create your views here.

def home(request):
    profiles=Profile.objects.all()
    context={'profiles':profiles}
    return render(request,'index.html',context)