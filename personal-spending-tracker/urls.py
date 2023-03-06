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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from expenditure import views
from expenditure.views import ChangePasswordView
#import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/',views.sign_up,name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('feed/',views.feed, name='feed'),
    path('log_out/',views.log_out, name='log_out'),
    path('about/',views.about, name='about'),
    path('features/',views.features, name='features'),
    path('contact/',views.contact, name='contact'),
    path('news_page/',views.news_page, name='news_page'),
    path('notification_page/',views.notification_page, name='notification_page'),
    path('create_category/',views.CreateCategoryView.as_view(),name='create_category'),
    path('spending/', views.spending, name='spending'),
    path('notification_page/<int:id>',views.mark_as_read, name='mark_as_read'),
    path('settings/',views.view_settings,name='settings'),
    path('settings/toggle_notification',views.toggle_notification,name='toggle_notification'),
    #path('transactions/', views.list_transactions, name='list_transactions'),
    path('transactions/add/<int:request_id>/', views.add_transaction, name='add_transaction'),
    path('transactions/income/', views.list_incomings, name='list_incomings'),
    path('add_friend/',views.add_friend,name='add_friend'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('reports/',views.view_report,name='reports'),
    path('profile/', views.profile, name='user_profile'),
    path('friends/', views.friends, name='friends'),
    path('friends/friends_profile/<int:id>', views.show_friends_profile, name='friends_profile'),
    #path('friends_profile/', views.friends_profile, name='friends_profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

