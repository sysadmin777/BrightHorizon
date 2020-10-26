"""BrightHorizon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from main.views import home, signup, assign, viewgoals
from main import forms as mainforms
import django.contrib.auth.views as auth_views
from main import views as core_views

urlpatterns = [
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^account/changepassword/$', core_views.PasswordChangeView.as_view(), name='changepassword'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', signup, name='register'),
    url(r'^login/$',
        auth_views.LoginView.as_view(),
        {
            'template_name': 'login.html',
            'authentication_form': mainforms.BootstrapAuthenticationForm,
        },
        name='login'),
    url(r'^logout$',
        auth_views.LogoutView.as_view(),
        {
            'next_page': '',
        },
        name='logout'),
        
    path('assign/', assign, name='assign'),
    path('view/', viewgoals, name='viewgoals'),
    
]
