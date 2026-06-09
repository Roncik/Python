from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from eboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='eboard/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post/new/', views.new_post, name='new-post'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'),
    path('post/<int:post_id>/update/', views.update_post, name='update-post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete-post'),
    path('post/myposts/', views.myposts, name='myposts'),
    path('post/mycomments/', views.mycomments, name='mycomments'),
]