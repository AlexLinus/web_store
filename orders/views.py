from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Cart, OrderItem, Order
from store.models import Product
from decimal import Decimal
# Create your views here.
from django.shortcuts import reverse


def get_checkout(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    if request.method == 'GET':
        form = OrderForm()
        return render(request, 'checkout.html', context={'checkout_form': form, 'cart': cart})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = Order()
            new_order.save()
            new_order.items.add(cart)
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.email = form.cleaned_data['email']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.city = form.cleaned_data['city']
            new_order.address = form.cleaned_data['address']
            new_order.notes = form.cleaned_data['notes']
            new_order.total_price = int(cart.cart_total)
            new_order.save()
            del request.session['cart_id']
            del request.session['total']

            return HttpResponseRedirect(reverse('finish_checkout_url', kwargs={'order_id': new_order.id})) #т.к form_valid требует вернуть HTTP запрос, то нужно использовать httprresonseredirect, т.к reverse возвращает строку.
        else:
            return render(request, 'checkout.html', context={'checkout_form': form, 'cart': cart})


def finish_checkout(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'name': order.first_name, 'order_id': order_id}
    return render(request, 'finish_checkout.html', context)

def get_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
        print('Сработал Try!')
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        print('Сработал Except!')

    return render(request, 'cart.html', context={'cart': cart})

def add_to_cart_view(request):
    # мы перенесли этот код в метод модели new_item, _ = OrderItem.objects.get_or_create(product=product, price=product.price) #Здесь мы создаем новый Item корзины. Т.к get_or_create возвращает кортеж а не отдельный объект, (объект, True или False) создалось или нет. То мы присваиваем так его new_item, _ =
    try:
        print('Сработало Try!')
        cart_id = request.session['cart_id'] #Присваиваем переменной cart_id, значение которое есть сейчас в сессии по такомк ключу cart_id. Грубо говоря, мы вынимаем id-шник.
        cart = Cart.objects.get(id=cart_id) #Здесь мы пытаемся взять корзину по тому id-шнику, который мы выняли из сессии.
        request.session['total'] = cart.items.count() #Здесь мы создаем в сессии, ещё одно значение, которое находится по ключу total. Это то количество наименований товара, которое находится в корзине.
    except:
        print('Сработало Except')
        cart = Cart() #Если то что было в try не отработало, то есть корзины не было до этого создано в сессии. То мы создаем новый экземпляр корзины.
        cart.save() #Сохраняем
        cart_id = cart.id #Здесь мы переменной cart_id присваиваем id нашей корзины.
        request.session['cart_id'] = cart_id #В сессию записываем в ключ cart_id - id этой корзины из переменной cart_id.
        cart = Cart.objects.get(id=cart_id) #Далее мы уже берем по этому значению саму корзину.
        #Если except отработал, то есть мы добавили свой первый товар в корзину. То далее уже при добавлении нового товара, будет обрабатываться блок try, т.к корзина будет уже существовать. То есть новой корзины создаваться уже не будет.
    product_slug = request.GET.get('product_slug') #Берем значение product_slug из ajax запроса, смотри в шаблонах.
    product = Product.objects.get(slug=product_slug) #Здесь мы получаем продукт из базы данных, который мы добавляем в корзину. По слагу.
    cart.add_to_cart(product)
    return JsonResponse({'cart_total': cart.items.count()})

def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id'] #Присваиваем переменной cart_id, значение которое есть сейчас в сессии по такомк ключу cart_id. Грубо говоря, мы вынимаем id-шник.
        cart = Cart.objects.get(id=cart_id) #Здесь мы пытаемся взять корзину по тому id-шнику, который мы выняли из сессии.
        request.session['total'] = cart.items.count() #Здесь мы создаем в сессии, ещё одно значение, которое находится по ключу total. Это то количество наименований товара, которое находится в корзине.
    except:
        cart = Cart() #Если то что было в try не отработало, то есть корзины не было до этого создано в сессии. То мы создаем новый экземпляр корзины.
        cart.save() #Сохраняем
        cart_id = cart.id #Здесь мы переменной cart_id присваиваем id нашей корзины.
        request.session['cart_id'] = cart_id #В сессию записываем в ключ cart_id - id этой корзины из переменной cart_id.
        cart = Cart.objects.get(id=cart_id) #Далее мы уже берем по этому значению саму корзину.
        #Если except отработал, то есть мы добавили свой первый товар в корзину. То далее уже при добавлении нового товара, будет обрабатываться блок try, т.к корзина будет уже существовать. То есть новой корзины создаваться уже не будет.
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug) #Здесь мы получаем продукт из базы данных, который мы добавляем в корзину. По слагу.
    cart.remove_from_cart(product.slug)
    cart_total_price = cart.cart_total
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart_total_price})

def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_total_price = cart.cart_total
    return JsonResponse({'cart_total_price': cart_total_price}) #Передаем json объект, в наш jquery скрипт


def get_manager_panel(request):
    all_orders = Order.objects.all()
    total_all_orders = all_orders.count()
    new_orders = all_orders.filter(status__iexact='Принят в обработку')
    orders_in_proccess = all_orders.filter(status__iexact='Выполняется')
    paid_orders = all_orders.filter(status__iexact='Оплачен')
    context = {'new_orders': new_orders, 'orders_in_proccess': orders_in_proccess, 'paid_orders': paid_orders, 'total_all_orders': total_all_orders}
    return render(request, 'manager_panel.html', context)