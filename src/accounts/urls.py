from django.urls import path
from accounts import views

from django.contrib.auth import views as auth_views

from django.conf.urls import include


urlpatterns =[
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('terms/', views.TermsView, name='terms'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/check/', views.ProfileCheckView.as_view(), name='profile_check'),
    path('profile/delete/<slug>', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('manage/', views.ManageView.as_view(), name='management'),
    path('history/', views.OrderHistoryView.as_view(), name='history'),

    path('inquiry/', views.InquiryView.as_view(), name='Inquiry'),
    path('inquiry/complete/', views.InquiryCompleteView.as_view(), name='Inquiry_complete'),
    
    # path('user_create/', views.UserCreate.as_view(), name='user_create'),


    # path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    # path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    # path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'), #追加
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'), #追加
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'), #追加
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'), #追加


    #Still
    # path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    # path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),


    # ソーシャルログイン
    # path('login2/', auth_views.LoginView.as_view(), name='login'),
    # path('logout2/', auth_views.LogoutView.as_view(), name='logout'),
    # path('index', views.index, name='index'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    # path('social/', views.index, name='social_page')
    
]