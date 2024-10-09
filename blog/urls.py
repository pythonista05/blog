from django.urls import path
from django.contrib.auth import views as authviews
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog_detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('like/<int:comment_id>', views.like_comment, name='like_comment'),
    path('share/<int:blog_id>', views.share_blog, name='share_blog'),
    path('search/', views.search, name='search'),
]
