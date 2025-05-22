from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('login/', views.login_user, name='login'),
   path('logout/', views.logout_user, name='logout'),
   path('register/', views.register_user, name='register'),
   path('update_password/', views.update_password, name='update_password'),
   path('update_user/', views.update_user, name='update_user'),
   path('update_info/', views.update_info, name='update_info'),
   path('product/<int:pk>', views.product, name='product'),
   path('category/<str:foo>', views.category, name='category'),
   path('category_summary/', views.category_summary, name='category_summary'),
   path('search/', views.search, name='search'),
   path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
   path('my_orders/', views.my_orders, name='my_orders'),
]
