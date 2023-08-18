from django.urls import path
from . import views

urlpatterns = [
    path('add_password', views.add_password, name= 'add_password'),
	path('delete_metadata', views.delete_metadata, name= 'delete_metadata'),
	path('add_signature', views.add_signature, name= 'add_signature'),
	path('optimize_file', views.optimize_file, name= 'optimize_file'),
]