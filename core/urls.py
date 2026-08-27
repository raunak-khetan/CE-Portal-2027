from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.prelimspage, name='prelimspage'),

    
   # path('about/', views.about_alcher, name='about_alcher'),

    # CFA Registration Steps
    path('cfa/', views.cfa_register_step1, name='cfa_register'),

    path('cfa/register/step1/', views.cfa_register_step1, name='cfa_step1'),
    path('cfa/register/step2/', views.cfa_step2_view, name='cfa_step2'),
    path('cfa/step-3/', views.cfa_step3, name='cfa_step3'),

    # Competitions page
    path('competitions/', views.prelimspage, name='competitions'),


    # Additional URLs from remote branch
    #path('', views.prelimspage, name='prelimspage'),
    path('competitions/<str:city_name>/', views.citypage, name='citypage'),
    path('competitions/<str:city_name>/<str:event_name>/', views.detailspage, name='detailspage'),
    path('competitions/<str:city_name>/<str:event_name>/register', views.registrationpage, name='registrationpage'),
    path('get-events/<str:city_name>/', views.get_city_events, name='get_city_events'),
    path('api/cities/', views.city_list, name='city_list'),
]

