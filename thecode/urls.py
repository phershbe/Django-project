from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('register/', views.registerpage, name='registerpage'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('search/', views.searchpage, name='searchpage'),
    path('profilecreate/', views.profilecreate, name='profilecreate'),
    path('profileupdate/', views.profileupdate, name='profileupdate'),
    path('messages/', views.messagespage, name='messagespage'),
    path('writemessage/<str:id>', views.writemessage, name='writemessage'),
    path('conversation/<str:id>', views.conversationpage, name='conversationpage'),
    path('searchwritemessage/<str:id>', views.searchwritemessage, name='searchwritemessage'),
]
