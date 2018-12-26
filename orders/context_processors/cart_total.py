from django.template.context_processors import request

def get_cart_total(request):
    if 'total' in request.session:
        return {'cart_total': request.session['total']}
    else:
        return {'cart_total': 0}