"""
URL configuration for my_site_sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from event_app import views

urlpatterns = [
    path('', views.event_index, name='index'),

    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),

    path('logout/', views.log_out, name="logout"),

    path('about', views.event_about, name="about"),

    path('contact', views.event_contact, name="contact"),

    path('signin', views.event_signin, name="signin"),
    path('signup', views.event_signup, name="signup"),


    path('type_add', views.events_type, name="type_add"),


    path('event_item', views.event_categories, name='event_item'),

    path('category/<int:category_id>/companies/', views.category_companies, name='category_companies'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view
    (template_name='forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view
    (template_name='forgot_password/password_reset_confirm.html'),name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view
    (template_name='forgot_password/password_reset_complete.html'), name='password_reset_complete'),


    path('profile/', views.edit_company_profile, name='profile'),
    path('companies', views.companylist, name="companies"),

    path('search/', views.search_companies, name='search_companies'),
    path('compview/<int:id>/', views.single_company_view, name='compview'),
    path('success/', views.success_view, name='success'),

    path('add_gallery_photo/', views.add_gallery_photo, name='add_gallery_photo'),
    path('display_gallery/<int:company_id>/', views.display_gallery, name='display_gallery'),

    path('company/chat/<int:company_id>/', views.chat_with_company, name='chat_with_company'),
    path('contact-list/', views.contact_list, name='contact_list'),
    path('reply/<int:message_id>/', views.reply_to_message, name='reply_to_message'),

    path('chat/<str:username>/', views.chat_with_user, name='chat_with_user'),

    path('company/<int:company_id>/book/', views.book_with_company, name='book_with_company'),
    # URL pattern for booking success page (optional)

    path('company/bookings/', views.company_bookings, name='company_bookings'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='delete_booking'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),

    path('booking/<int:booking_id>/select-payment/', views.select_payment_option, name='select_payment_option'),
    path('booking/<int:booking_id>/debit-card-payment/', views.debit_card_payment, name='debit_card_payment'),
    path('booking/<int:booking_id>/net-banking-payment/', views.net_banking_payment, name='net_banking_payment'),
    path('booking/success/', views.payment_success, name='payment_success'),

    path('payments/', views.display_payments, name='payments'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),

    path('notifications/', views.notifications, name='notifications'),
    path('notification_count/', views.notification_count, name='notification_count'),
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),

    path('u_profile/', views.profile, name='user_profile'),
    path('booking/history/', views.booking_history, name='booking_history'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking2'),


    path('view_chats/', views.view_chats, name='view_chats'),
    path('unread_message_count/', views.unread_message_count, name='unread_message_count'),

]

