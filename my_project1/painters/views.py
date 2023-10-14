from django.shortcuts import render, redirect
# from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Painter
from .forms import PainterForm

# painters = [
#     {'id':1, 'name': 'Picasso_1'},
#     {'id':2, 'name': 'Picasso_2'},
#     {'id':3, 'name': 'Picasso_3'},
# ]

def chat(request):
    return render(request, 'painters/chat.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Юзер не найден')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Юзер не найден | в пароле ошибка')
    
    return render(request, 'login_register.html', {'page': "login"})


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при регистрации')
    return render(request, 'login_register.html', {'page': "register", 'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    # return HttpResponse('Home page')
    painters = Painter.objects.all()
    context = {'painters': painters}
    return render(request, 'home.html', context)


def painter(request, pk):
    # return HttpResponse('Painter')
    
    # painter = None    
    # for i in painters:
    #     if i['id'] == int(pk):
    #         painter = i

    painter = Painter.objects.get(id=pk)
    context = {'painter': painter}
    return render(request, 'painter.html', context)

@login_required(login_url='login')
def painter_form(request):
    form = PainterForm()
    # context = {'form': form}
    if request.method == 'POST':
        form = PainterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "painter_form.html", {'form': PainterForm()})


def painter_update(request, pk):
    painter = Painter.objects.get(id=pk)
    form = PainterForm(instance=painter)
    if request.method == 'POST':
        form = PainterForm(request.POST, instance=painter)
        if form.is_valid():
            form.save()
            return redirect('home')            
    return render(request, "painter_form.html", {'form': form})


def painter_delete(request, pk):
    painter = Painter.objects.get(id=pk)
    if request.method == 'POST':
        painter.delete()
        return redirect('home')
    return render(request, "delete.html", {'painter': painter})