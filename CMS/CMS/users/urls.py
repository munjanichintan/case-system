from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index, name='index'),
	path('signup', views.signup, name='signup'),
    path('signin', views.signin, name="signin"),
   	path('logout/', auth_views.LogoutView.as_view(template_name='users/index.html'), name='logout'),
]