from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Painter, Raiting, Message
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
            messages.error(request, 'В пароле ошибка')
    
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
    painter_count = painters.count()
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    painters = Painter.objects.filter(
        Q(user__username__icontains = q) |
        Q(raiting__raiting__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    painterFilter_count = painters.count()

    raitings = Raiting.objects.all()
    users = User.objects.all()
    comments = Message.objects.filter(
        Q(painter__name__icontains = q) |
        Q(body__icontains = q)
    )

    context = {
        'painters': painters, 
        'raitings': raitings, 
        'users': users,
        'comments': comments,
        'painter_count': painter_count,
        'painterFilter_count': painterFilter_count,
        'action_url': 'home',
    }

    # if (painter_count != painterFilter_count):
    #     context = {
    #         'painters': painters, 
    #         'raitings': raitings, 
    #         'users': users,
    #         'painter_count': painter_count,
    #         'painterFilter_count': painterFilter_count
    #     }
    # else:
    #     context = {
    #         'painters': painters, 
    #         'raitings': raitings, 
    #         'users': users,
    #         'painter_count': painter_count,
    #         'painterFilter_count': ''
    #     }

    return render(request, 'home.html', context)


def userProfile(request, pk):
    username = User.objects.get(id=pk)
    painters = username.painter_set.all()
    painter_message = username.message_set.all()
    raitings = Raiting.objects.all()
    return render(request, 'profile.html', {'username': username, 'painters': painters, 'painter_message': painter_message, 'raitings': raitings})


def painter(request, pk):
    # return HttpResponse('Painter')
    
    # painter = None    
    # for i in painters:
    #     if i['id'] == int(pk):
    #         painter = i
    painter = Painter.objects.get(id=pk)

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            painter=painter,
            body=request.POST.get('body')
        )
        painter.participants.add(request.user)
        return redirect('painter', pk=painter.id)
    
    # comments = painter.message_set.all().order_by('-created')
    method = request.method
    # comments = painter.message_set.all()
    participants = painter.participants.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    comments = painter.message_set.filter(body__icontains = q)
    # painters = Painter.objects.filter(raiting__raiting__icontains = q)
    
    
    context = {
        'method': method, 
        'painter': painter, 
        'comments': comments, 
        'participants': participants,
        'painter_id': painter.id,
        'q': q
    }
    return render(request, 'painter.html', context)


@login_required(login_url='login')
def painter_form(request):
    form = PainterForm()
    # context = {'form': form}
    if request.method == 'POST':

        # form = PainterForm(request.POST)
        # if form.is_valid():
        #     form = form.save(commit=False)
        #     form.user = request.user
        #     form.save()
        #     return redirect('home')

        form = PainterForm(request.POST, instance=Painter(user=request.user))
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


@login_required(login_url='login')
def painter_delete(request, pk):
    painter = Painter.objects.get(id=pk)
    if request.method == 'POST':
        painter.delete()
        return redirect('home')
    return render(request, "delete.html", {'painter': painter})


@login_required(login_url='login')
def comment_delete(request, pk):
    comment = Message.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('Ошибка доступа')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    
    return render(request, "delete.html", {'comment': comment, 'comment_page': True})