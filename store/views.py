from django.shortcuts import render
from .models import Product, Category, ProductImage
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    newest = Product.objects.filter(is_active=True, available=True)[:6]
    return render(request, 'index.html', context={'products': newest })


def get_product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug__iexact=product_slug, category__slug__iexact=category_slug)
    return render(request, 'product_detail.html', context={'product': product})

def get_category_detail(request, category_slug):
    category = get_object_or_404(Category, slug__iexact=category_slug)
    items = Product.objects.filter(category__exact=category)
    print(items)
    paginator = Paginator(items, 9)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    print(paginator)

    return render(request, 'category_detail.html', context={'category': paginator.page(page)})

def search_form(request):
    search_query = request.GET.get('searchproduct', '')
    if search_query:
        products = Product.objects.filter(title__icontains=search_query, is_active=True)
        if products:
            return render(request, 'search.html', context={'products': products, 'search_query': search_query})
        else:
            #categories = Category.objects.filter(title__icontains=u'{}'.format(search_query)) #Не работает. Регистрозависимый запрос. Пока не понял как исправить.
            #Короч contain в sqlite не будет работать. Только в других базах. Поэтому делаю через словари.
            categories_all = Category.objects.all()
            for category in categories_all:
                if search_query in str(category).lower():
                    categories = category
                    print(categories)
                    break
            #ЕЕе бой я сделл это! Теперь всё работает хорошо! Ищет и по категориям, если по продуктам не нашло.

            if categories:
                products = Product.objects.filter(category__exact=categories)
                return render(request, 'search.html', context={'products': products, 'search_query': search_query})
            else:
                print(Category.objects.filter(title__icontains=search_query).query)
                return render(request, 'search.html', context={'search_query': search_query, 'search_alert': 'Извините, но мы не смогли ничего найти по запросу "{}". Попробуйте поискать что-нибудь другое.'.format(search_query)})
    else:
        return render(request, 'search.html', context={'search_query': '', 'search_alert': 'Извините, но вы ничего не указали для поиска!'})

