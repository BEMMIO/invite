from django.urls import path

from .import views


urlpatterns = [
    path('app/',views.app,name='app'),
    path('login/',views.user_login,name='user-login'),
    path('log-out/',views.user_logout,name='user-logout'),
    path('new-user/<str:random>/<str:code>/',views.new_user_registered,name='new-user'),

]


app_name = "account"