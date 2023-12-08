from django.urls import path
from .views import glucose_reading_list, glucose_reading_graph, login_view, register, logout_view


urlpatterns = [
    path('glucose_reading/', glucose_reading_list, name='glucose_reading_list'),
    path('glucose_graph/', glucose_reading_graph, name='glucose_graph'),
    path('', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]
