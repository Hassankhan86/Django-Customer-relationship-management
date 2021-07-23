from django.shortcuts import render,redirect
# Create your views here.
from django.http import HttpResponse
from accounts.models import *
from .forms import OrderForm
from  .filters import OrderFilter


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'customers': customers, 'orders': orders, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    product = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': product})


def customers(request, pk_test):

    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs


    context = {'customer': customer, "orders": orders,'myFilter':myFilter,
               "order_count":order_count,}
    return render(request, 'accounts/customers.html', context)


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect('/')
    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request,pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return  redirect('/')

    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return  redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)
