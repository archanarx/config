from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'tracker/home.html')



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created! Please login.")
            return redirect('login')

    return render(request, 'tracker/signup.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login details")

    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


from .models import WaterIntake
from django.db import IntegrityError

@login_required
def add_intake(request):
    if request.method == 'POST':
        quantity = request.POST['quantity']
        try:
            WaterIntake.objects.create(
                user=request.user,
                quantity=quantity
            )
            messages.success(request, "Water intake added!")
            return redirect('home')
        except IntegrityError:
            messages.error(request, "You already added water intake today!")

    return render(request, 'tracker/add_intake.html')


from django.core.paginator import Paginator

@login_required
def intake_list(request):
    intakes = WaterIntake.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(intakes, 5)  # 5 records per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/intake_list.html', {'page_obj': page_obj})


from django.shortcuts import get_object_or_404

@login_required
def edit_intake(request, id):
    intake = get_object_or_404(WaterIntake, id=id, user=request.user)

    if request.method == 'POST':
        intake.quantity = request.POST['quantity']
        intake.save()
        return redirect('list')

    return render(request, 'tracker/edit_intake.html', {'intake': intake})


@login_required
def delete_intake(request, id):
    intake = get_object_or_404(WaterIntake, id=id, user=request.user)
    intake.delete()
    return redirect('list')


@login_required
def compare_intake(request):
    result = None

    if request.method == 'POST':
        date1 = request.POST['date1']
        date2 = request.POST['date2']

        intake1 = WaterIntake.objects.filter(user=request.user, date=date1).first()
        intake2 = WaterIntake.objects.filter(user=request.user, date=date2).first()

        if intake1 and intake2:
            result = abs(intake1.quantity - intake2.quantity)
        else:
            messages.error(request, "No data found for one or both dates")

    return render(request, 'tracker/compare.html', {'result': result})
