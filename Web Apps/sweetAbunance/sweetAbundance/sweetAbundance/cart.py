from django.conf import settings

from .models import Product

class CartSession(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def add(self, product, quantity=1, size=2.0, update_quantity=False):
        product = str(product)

        if product not in self.cart:
            self.cart[product] = {'quantity': quantity, 'id': product, "size": size}
        else:
            self.cart[product]['quantity'] = float(self.cart[product]["quantity"]) + float(quantity)
        
        if update_quantity:
            self.cart[product]['quantity'] += float(quantity)

            if self.cart[product]['quantity'] == 0:
                self.remove(product)
            
        self.save()

    def update(self, product, quantity, size):
        product = str(product)

        if product not in self.cart:
            self.cart[product] = {'quantity': quantity, 'id': product, "size": size}
        else:
            self.cart[product]['quantity'] = float(quantity)
            self.cart[product]['size'] = size
        
        if self.cart[product]['quantity'] == 0:
            self.remove(product)
            
        self.save()
    
    def remove(self, product):
        if product in self.cart:
            del self.cart[product]
            self.save()
    
    def clear(self):
        self.cart = {}
        self.save()