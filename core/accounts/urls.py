from django.urls import path  
from . import views
urlpatterns = [
    
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('logout', views.logout , name='logout'),
    path('dashboard', views.dashboard , name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate , name='activate'),
    path('', views.dashboard , name='dashboard'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpasssword_validate , name='resetpassword_validate'),
    path('my_order',views.my_order,name='my_order'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('change_password',views.change_password,name='change_password'),
    
]




