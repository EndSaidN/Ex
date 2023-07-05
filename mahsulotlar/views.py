from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from mahsulotlar.models import Product
from akkauntlar.models import Orders
from mahsulotlar.models import Category


class Cart(View):
    def get(self, request):
        product_id = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(product_id)
        return render(request, 'mahsulotlar/cart.html', {'products': products})


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Orders.get_orders_by_customer(customer)
        return render(request, 'akkauntlar/orders.html', {'orders': orders})


class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {product: 1}

        request.session['cart'] = cart
        return redirect('home')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    categories = Category.get_all_categories()
    category = request.GET.get('category')
    if category:
        products = Product.get_all_products_by_categoryid(categories)
    else:
        products = Product.get_all_products()

    data = dict()
    data['products'] = products
    data['categories'] = categories

    return render(request, 'mahsulotlar/index.html', data)
