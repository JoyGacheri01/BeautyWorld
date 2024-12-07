from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('home/', views.home, name='home'),
    # path('logout/', views.logout, name='logout'),

]
