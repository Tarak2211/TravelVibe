from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('destinations/', views.destinations_view, name='destinations'),
    path('packages/', views.packages_view, name='packages'),
    path('packages/<int:package_id>/', views.package_detail_view, name='package_detail'),
    path('packages/<int:package_id>/book/', views.create_booking_view, name='create_booking'),
    path('about/', views.about_view, name='about'),
    path('budget-planner/', views.budget_planner_view, name='budget_planner'),
]
