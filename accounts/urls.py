from  django.urls import  path
from . import  views

app_name = 'accounts'


urlpatterns = [
    path('login', views.loginpage, name='login'),
    path('register', views.registerpage, name='register'),
    path('logout', views.logoutUser, name='logout'),

    path('', views.home,name='home'),
    path('user/', views.userpage,name='user'),
    path('setting/', views.accountsetting, name='setting'),

    path('products/', views.products,name='products'),
    path('customers/<str:pk_test>', views.customers,name='customers'),

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),



]
