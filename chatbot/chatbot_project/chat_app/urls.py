from django.urls import path
from . import views


urlpatterns =[
    path('', views.chatbot,name='chatbot'),
    path('status',views.check_response_status,name='status'),
    path('login', views.login,name='login'),
     path('logout', views.logout,name='logout'),
    path('register', views.register,name='register')
]