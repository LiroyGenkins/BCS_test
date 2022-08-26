from django.urls import path

from . import views

app_name = 'transact'
urlpatterns = [
    path('', views.transaction_send, name = 'transaction_send'),
    path('', views.index, name = 'index'),
    path('<int:transaction_id>/', views.detail, name = 'detail')
]