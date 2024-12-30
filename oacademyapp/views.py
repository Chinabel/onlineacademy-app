from datetime import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Course, Assignment, Todo, Profile, Book, YouTubeVideo
from .forms import ProfileForm, TodoForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def oacademyapp(request):
    return render(request, 'home.html', {})

def home(request):
    """
    Home page view.
    """
    courses = Course.objects.all()
    assignments = Assignment.objects.all()

    return render(request, 'home.html', {'courses': courses, 'assignments': assignments})

def index(request):
    items = items.object.order_by("-publish_date")
    now = timezone.now()
    return render(request,'portfolio/index.html', {"items": items, "year": now.year})

def courses(request):
    """
    View to list all available courses.
    """
    course_list = Course.objects.all()
    return render(request, 'courses.html', {'courses': course_list})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(request, 'course_detail.html', {'course': course})


def assignments(request):
    """
    View to list all assignments.
    """
    assignment_list = Assignment.objects.all()
    return render(request, 'assignments.html', {'assignments': assignment_list})


def assignment_detail(request, id):
    assignment = get_object_or_404(Assignment, id=id)

    return render(request, 'assignment_detail.html', {'assignment': assignment})

def youtube_video_list(request):
    videos = YouTubeVideo.objects.all()

    return render(request, 'youtube_video_list.html', {'videos': videos})


def todo(request):
    """
    View to manage and display to-do items for the logged-in user.
    """
    todo_list = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {'todos': todo_list})


def todo_list(request):
    todo = Todo.objects.all()
    return render(request, 'todo_list.html', {'todo': todo})

def todo_detail(request, id):
    todo = Todo.objects.get(id=id)
    return render(request, 'todo_detail.html', {'todo': todo})

def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('todo')  # Redirect to the todos list page
    else:
        form = TodoForm()
    return render(request, 'add_todo.html', {'form': form})


def books(request):
    """
    View to list all books available in the academy.
    """
    book_list = Book.objects.all()
    return render(request, 'book.html', {'books': book_list})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    return render(request, 'book_detail.html', {'book': book})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')  # Redirect to 'next' URL after login
            return redirect(next_url)
        else:
            return HttpResponse("Invalid credentials", status=401)
        
    return render(request, 'login.html')


def logout_view(request):
    """
    View to handle user logout.
    """
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def profile(request):
    try:
        user_profile = request.user.profile
    except ObjectDoesNotExist:
        return redirect('create_profile')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving the form
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})


def about(request):
    return render(request, 'about.html')