from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import CreateUserForm,LoginForm,CreateR,UpdateR
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Record_customer
# Create your views here.

def home(request):
  
  return render(request,"webapp/index.html")


def register(request):
  form = CreateUserForm()
  if request.method=="POST":
    form=CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("my-login")
  context={'form':form}   
  return render(request,"webapp/register.html", context=context)


def my_login(request):
  form=LoginForm();
  if request.method=='POST':
    form=LoginForm(request, data=request.POST)
    if form.is_valid():
      username=request.POST.get('username')
      password=request.POST.get('password')
      user=authenticate(request,username=username,password=password)
      if user is not None:
        auth.login(request,user)
        return redirect('dashboard')
  context={'form':form}  
  return render(request,'webapp/my-login.html', context=context)  


def user_logout(request):

  auth.logout(request)
  return redirect("my-login")


@login_required(login_url='my-login')
def dashboard(request):
  my_records=Record_customer.objects.all()

  context ={'records': my_records}

  return render(request, 'webapp/dashboard.html', context=context)


@login_required(login_url='my-login')
def create_record(request):
  form = CreateR()

  if request.method == "POST":

        form = CreateR(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, " record created!")

            return redirect("dashboard")

  context = {'form': form}

  return render(request, 'webapp/create-record.html', context=context)


@login_required(login_url='my-login')
def update_record(request,pk):
  record=Record_customer.objects.get(id=pk)
  form=UpdateR(instance=record)
  if request.method=="POST":
    form=UpdateR(request.POST,instance=record)
    if form.is_valid():
      form.save()
      return redirect("dashboard")
  context={'form':form}  
  return render(request, 'webapp/update-record.html',context)


@login_required(login_url='my-login')
def view_record(request,pk):
  all_records=Record_customer.objects.get(id=pk)

  context={'record':all_records}

  return render(request,'webapp/view-record.html',context)


@login_required(login_url='my-login')
def delete_record(request,pk):
  record=Record_customer.objects.get(id=pk)
  record.delete()

  return redirect('dashboard')

