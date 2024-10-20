from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('select_filter/<str:image_name>/', views.select_filter, name='select_filter'),
    path('view_image/<str:image_name>/', views.view_image, name='view_image'),
]
