from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add-user/', views.add_user, name='add_user'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('agents/', views.agents, name='agents'),
    path('add-agents/', views.add_agents, name='add_agents'),
    path('edit_agent/<int:id>/', views.edit_agent, name='edit_agent'),
    path('delete_agent/<int:id>/', views.delete_agent, name='delete_agent'),
    path('account/', views.accounts, name='account'),
]