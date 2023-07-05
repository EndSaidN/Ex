from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views import View
from akkauntlar.models import Customer
from akkauntlar.models import Orders
from mahsulotlar.models import Product
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'akkauntlar/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print(email, password)
        return render(request, 'akkauntlar/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Signup(View):
    def get(self, request):
        return render(request, 'akkauntlar/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone_number = postData.get('phone_number')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone_number=phone_number,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'akkauntlar/signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone_number:
            error_message = 'Enter your Phone Number'
        elif len(customer.phone_number) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'

        return error_message


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))

        for product in products:
            order = Orders(customer=Customer(id=customer),
                           product=product,
                           price=product.price,
                           address=address,
                           phone_number=phone_number,
                           quantity=cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}
        return redirect('cart')
