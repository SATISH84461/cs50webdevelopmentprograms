from django.urls import path
from . import views

urlpatterns = {
    path('/home',views.index,name='index'),
    path('/menu',views.menu,name='menu'),
    path('/aboutus',views.aboutus,name='aboutus'),
    path('/contact',views.contact,name='contact'),
}