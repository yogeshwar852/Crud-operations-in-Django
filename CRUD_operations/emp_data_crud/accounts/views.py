from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, OrderForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import EmpInfo

User = get_user_model()
# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')

def employee_insert(request):
    form = RegisterForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password_first')
        User.objects.create_user(username, email, password)
        return redirect('User_list')
    else:
        return render(request, 'accounts/register.html', context=context)

# def empdata(request):
#     return render(request, 'accounts/index.html')

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            print('allaaaa')
            login(request, user)
            return redirect('User_list')

    return render(request, 'accounts/login.html', context=context)

  # decorator
def register_page(request):
    form = RegisterForm(request.POST or None)    #we specify which form to use for registration
    context = {'form':form}        #we made context  dictionary which contains form as value
    if form.is_valid():
        username = form.cleaned_data.get('username')      # in the brackets we have the model name and
        email = form.cleaned_data.get('email')             # object made is of our any name but to keep it
        password = form.cleaned_data.get('password_first')       #clear we give same fields name

        User.objects.create_user(username=username, email= email, password= password)
        emp = EmpInfo(username=username,email= email,password_first= password, password_again=password) #we created object emp for storing all the info in it from models EmpInfo and save it
        emp.save()   #this is most imp part that connect our forms to models which tells to go all data in the EmpInfo
        return redirect('/')
    else:
        return render(request, 'accounts/register.html', context=context)

class User_list(View):
    def get(self, request, *args, **kwargs):
        print('alla ka')
        empinfo = EmpInfo.objects.all()
        return render(request, "accounts/data.html", {'empdata':empinfo })

def update_order(request, pk):
    order = EmpInfo.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/data.html', {'empdata': EmpInfo.objects.all()})  #we pas  key as table name
        # return redirect("accounts/data.html", {'empdata': EmpInfo.objects.all()})

    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)

def delete_Order(request, pk):
    order = EmpInfo.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return render(request, 'accounts/data.html', {'empdata': EmpInfo.objects.all()})
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


def logout_page(request):
    logout(request)
    return redirect('/')




