from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index',),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    
]
