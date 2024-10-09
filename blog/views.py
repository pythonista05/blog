from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import CustomLoginForm, CustomSignupForm
from django.core.paginator import Paginator
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.db.models import Q
from django import forms
from .models import Comment
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  
    else:
        form = CustomSignupForm()
    
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('blog_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.success(request, 'logout successful')
    return redirect('login')

@login_required
def blog_list(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("_______________",blogs)
    return render(request, 'blog_list.html', {'page_obj': page_obj})

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comment_form = CommentForm()
    return render(request, 'blog_detail.html', {'blog': blog, 'comment_form':comment_form})

@login_required
def search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Blog.objects.raw(
            'SELECT * FROM blog_blog WHERE MATCH(title, content) AGAINST(%s IN NATURAL LANGUAGE MODE)', [query]
        )
    else:
        posts = Blog.objects.none()

    return render(request, 'search.html', {'posts': posts, 'query': query})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

@login_required
def add_comment(request, blog_id):
    try:
        blog = get_object_or_404(Blog, id=blog_id)
        if request.method == 'POST':
            print("____")
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blog = blog
                comment.author = request.user
                comment.save()
                return redirect('blog_detail', blog_id=blog.id)
        return redirect('blog_detail', blog_id=blog.id)  
    except Exception as e:
        pass


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog_detail', blog_id=comment.blog.id)


def share_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        email = request.POST['email']
        try:
            send_mail(
                f"Check out this blog: {blog.title}",
                blog.content,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Email sent successfully!')
        except Exception as e:
            messages.error(request, f'Error sending email: {e}')
        return redirect('blog_detail', blog_id=blog.id)
    return render(request, 'share_blog.html', {'blog': blog})