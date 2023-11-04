from django.urls import path
from . import views
    
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('chat/', views.chat, name="chat"),

    path('', views.home, name="home"),
    path('painter/<str:pk>/', views.painter, name="painter"),
    path('comment_delete/<str:pk>/', views.comment_delete, name='commentDelete'),

    path('painter_form/', views.painter_form, name="painterForm"),
    path('painter_update/<str:pk>/', views.painter_update, name="painterUpdate"),
    path('painter_delete/<str:pk>/', views.painter_delete, name="painterDelete"),
]