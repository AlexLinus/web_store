from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Cart, OrderItem
from store.models import Product
from decimal import Decimal
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

def add_to_cart_view(request):
    # мы перенесли этот код в метод модели new_item, _ = OrderItem.objects.get_or_create(product=product, price=product.price) #Здесь мы создаем новый Item корзины. Т.к get_or_create возвращает кортеж а не отдельный объект, (объект, True или False) создалось или нет. То мы присваиваем так его new_item, _ =
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
    return JsonResponse({'cart_total': cart.items.count()})

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
    cart_item = OrderItem.objects.get(id=int(item_id))
    cart_item.quantity = int(qty)
    cart_item.price = int(qty) * Decimal(cart_item.product.price)
    print("Итоговая стоимость: {}".format(cart.total_cart_price))
    print(qty, item_id, cart_item.price)
    cart_item.save()
    cart.save()
    cart_total_price = cart.cart_total
    return JsonResponse({'cart_total_price': cart_total_price}) #Передаем json объект, в наш jquery скрипт


#Недосмотрел урок 23. Там короче, если десятки товаров. В частности 80, Decimal выдает ошибку какую-то, скорей всего слишком большая цифра получается. Разобраться. Может переопределить класс Decimal