from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from accounts.models import *
from .forms import OrderForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from .decorators import unauthenticated_user, allowed_users, admin_only

from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, "Username Or Password is Incorrect ")
    return render(request, 'accounts/login.html', )


@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )

            messages.success(request, 'Accounts was created for ' + username)
            return redirect('accounts:login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='/login')
# @allowed_users(allowed_role=['admin'])
@admin_only
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


@login_required(login_url='/login')
@allowed_users(allowed_role=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_role=['customer'])
def accountsetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)


    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, 'accounts/accounts_setting.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_role=['admin'])
def products(request):
    product = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': product})


@login_required(login_url='/login')
@allowed_users(allowed_role=['admin'])
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, "orders": orders, 'myFilter': myFilter,
               "order_count": order_count, }
    return render(request, 'accounts/customers.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_role=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_role=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_role=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
