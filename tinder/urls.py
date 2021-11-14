from django.urls import path
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns
from tinder import views

urlpatterns = [
    path('clients/create', views.CreateClientView.as_view(), name='register'),
    path('clients/login/', views.LoginAPI.as_view(), name='login'),
    path('clients/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('clients/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('clients/all', views.ClientListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
