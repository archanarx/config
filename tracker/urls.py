from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_intake, name='add'),
    path('list/', views.intake_list, name='list'),
    path('edit/<int:id>/', views.edit_intake, name='edit'),
    path('delete/<int:id>/', views.delete_intake, name='delete'),
    path('compare/', views.compare_intake, name='compare'),

]
