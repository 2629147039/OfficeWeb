from django.urls import path
from managent import views


app_name = 'managent'


urlpatterns = [
    path('companyFlow_sel/<int:pn>/', views.companyFlow_sel, name='companyFlow'),
    path('', views.index),
    path('message_del/<int:id>/', views.message_del, name="messageDel"),
    path('message_add/', views.message_add, name="add"),
]