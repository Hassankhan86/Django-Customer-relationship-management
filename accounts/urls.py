from  django.urls import  path
from . import  views

app_name = 'accounts'


urlpatterns = [
    path('', views.home,name='home'),
    path('products/', views.products,name='products'),
    path('customers/<str:pk_test>', views.customers,name='customers'),

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),

]