from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'address', 'notes', 'buying_type']

    #Далее мы переопределям __init__ класс формы, где указываем для каждого поля класс и плейсхолдер, куда помещаем label поля
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
            field.widget.attrs['placeholder'] = field.label