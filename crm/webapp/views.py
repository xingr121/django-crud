from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateUserForm,LoginForm
# Create your views here.

def home(request):
  
  return render(request,"webapp/index.html")


