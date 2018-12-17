from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Cart, OrderItem
from store.models import Product
# Create your views here.
from django.shortcuts import reverse


def get_checkout(request):
    if request.method == 'GET':
        form = OrderForm()
        return render(request, 'checkout.html', context={'checkout_form': form})


def get_cart(request):
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

    return render(request, 'cart.html', context={'cart': cart})

def add_to_cart_view(request, product_slug):
    product = Product.objects.get(slug=product_slug) #Здесь мы получаем продукт из базы данных, который мы добавляем в корзину. По слагу.
    new_item, _ = OrderItem.objects.get_or_create(product=product, price=product.price) #Здесь мы создаем новый Item корзины. Т.к get_or_create возвращает кортеж а не отдельный объект, (объект, True или False) создалось или нет. То мы присваиваем так его new_item, _ =
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

    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()

    return HttpResponseRedirect(reverse('get_cart_url'))

def remove_from_cart_view(request, product_slug):
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

    product = Product.objects.get(slug=product_slug) #Здесь мы получаем продукт из базы данных, который мы добавляем в корзину. По слагу.
    for cart_item in cart.items.all():
        if cart_item.product == product:
            cart.items.remove(cart_item)
            cart.save()
            return HttpResponseRedirect(reverse('get_cart_url'))

#оСТАНОВИЛСЯ НА 18 УРОКЕ.