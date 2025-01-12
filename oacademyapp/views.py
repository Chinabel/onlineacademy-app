from datetime import timezone
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from onlineacademy.settings import LANGUAGES
from .models import Course, Assignment, Todo, Profile, Book, YouTubeVideo
from .forms import ProfileForm, TodoForm, ContactForm, ProfileForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _, activate
from django.views.decorators.http import require_GET

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
    return render(request, 'course_list.html', {'courses': course_list})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(request, 'course_detail.html', {'course': course})


@login_required(login_url='/login/')
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
    context = {'videos': videos}

    return render(request, 'youtube_video_list.html', context)


@login_required(login_url='/login/')
def todo(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated
    
    todo_list = Todo.objects.filter(user=request.user)
    return render(request, 'todo_list.html', {'todos': todo_list})


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
    return render(request, 'book_list.html', {'books': book_list})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    return render(request, 'book_detail.html', {'book': book})


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to the profile page if logged in

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile after successful registration
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
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect(reverse('profile'))
        else:
            return HttpResponse("Invalid credentials", status=401)
        
    return render(request, 'registration/login.html')

@login_required(login_url='/login/')
def profile(request):
    try:
        user_profile = request.user.profile
    except ObjectDoesNotExist:
        return redirect('profile_completion')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})

@login_required(login_url='/login/')
def profile_completion(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()

    return render(request, 'profile.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have successfully logged out.")
    else:
        messages.warning(request, "You are not logged in.")
    return redirect('home')

def logged_out(request):
    return render(request, 'logged_out.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            form.save()

            # Send a notification email
            subject = "New Contact Message"
            message = f"New message from {form.cleaned_data['name']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])

            # Redirect to a success page
            return redirect('contact:success')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

def success(request):
    return render(request, 'contact/success.html')

def set_language(request, lang_code):
    if lang_code not in dict(LANGUAGES):
        lang_code = 'en'
    activate(lang_code)
    return redirect(request.META.get('HTTP_REFERER', '/'))