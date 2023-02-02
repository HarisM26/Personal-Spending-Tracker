"""personal-spending-tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from expenditure import views
#import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/',views.register,name='register'),
    path('log_in/', views.log_in, name='log_in'),
    path('feed/',views.feed, name='feed'),
    path('log_out/',views.log_out, name='log_out'),
    path('about/',views.about, name='about'),
    path('features/',views.features, name='features'),
    path('contact/',views.contact, name='contact'),
    path('news_page/',views.news_page, name='news_page'),
    path('notification_page/',views.notification_page, name='notification_page'),
    path('create_category/',views.create_category,name='create_category'),
   # path('^inbox/notifications/',include(notifications.urls,namespace='notifications')),
]
