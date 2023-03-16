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
from expenditure.views import other_views, category_views, transaction_views, user_views, notification_views, report_views

# import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),

    # ========= Other urls ===========
    path('', other_views.home, name='home'),
    path('feed/', other_views.feed, name='feed'),
    path('features/', other_views.features, name='features'),
    path('settings/', other_views.view_settings, name='settings'),


    # ========= User urls ===========
    path('sign_up/', user_views.sign_up, name='sign_up'),
    path('log_in/', user_views.log_in, name='log_in'),
    path('log_out/', user_views.log_out, name='log_out'),
    path('add_friend/', user_views.add_friend, name='add_friend'),
    path('friends/', user_views.friends, name='friends'),
    path('friends/friends_profile/<int:id>',
         user_views.show_friends_profile, name='friends_profile'),
    path('friends/follow_toggle/<int:id>',
         user_views.follow_toggle, name='follow_toggle'),
    path('leaderboard/', user_views.leaderboard, name='leaderboard'),
    path('profile/', user_views.profile, name='user_profile'),
    path('password-change/', user_views.ChangePasswordView.as_view(),
         name='password_change'),
    path('forgot_password/', user_views.forgot_password, name='forgot_password'),


    # ========== Notification urls =============
    path('settings/toggle_notification',
         notification_views.toggle_notification, name='toggle_notification'),
    path('view_notification/<int:id>', notification_views.view_selected_notification,
         name='view_selected_notification'),
    path('notification_page/', notification_views.notification_page,
         name='notification_page'),


    # ========= Category urls ===========
    path('spending-category/<int:pk>/edit',
         category_views.EditSpendingCategoryView.as_view(), name='edit_spending_category'),
    path('spending-category/<int:pk>/delete',
         category_views.DeleteSpendingCategoryView.as_view(), name='delete_spending_category'),
    path('create_category/', category_views.CreateSpendingCategoryView.as_view(),
         name='create_category'),
    path('spending/', category_views.spending, name='spending'),
    path('income-category/<int:pk>/edit',
         category_views.EditIncomeCategoryView.as_view(), name='edit_income_category'),
    path('income-category/<int:pk>/delete',
         category_views.DeleteIncomeCategoryView.as_view(), name='delete_income_category'),
    path('create_incoming_category/', category_views.create_incoming_category,
         name='create_incoming_category'),
    path('incomings/', category_views.incoming, name='incomings'),


    # ========= Transaction urls ============
    path('transactions/add_income/<int:request_id>/',
         transaction_views.add_income_transaction, name='add_income_transaction'),
    path('transactions/income/',
         transaction_views.list_incomings, name='list_incomings'),
    path('incomings/edit/<int:id>/',
         transaction_views.edit_incoming_transaction, name='edit_income'),
    path('incomings/delete/<int:id>/',
         transaction_views.delete_incoming_transaction, name='delete_income'),
    path('transactions/add/<int:request_id>/',
         transaction_views.add_spending_transaction, name='add_spending_transaction'),
    path('spending/edit/<int:id>/',
         transaction_views.edit_spending_transaction, name='edit_spending'),
    path('spending/delete/<int:id>/',
         transaction_views.delete_spending_transaction, name='delete_spending'),
    path('transactions/<int:id>/',
         transaction_views.view_transaction, name='transaction'),



    # ========  Report urls ========

    path('reports/', report_views.view_report, name='reports'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
