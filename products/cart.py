from django.db.models import Q

from . import models
from .models import CartItem
from .promotion import Promotion

CART_ID = "CART-ID"


class Cart:
    """
    Cart class, this will have all methods like add, remove, etc related to a cart
    """

    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        cart = None
        if cart_id:
            query = Q(id=cart_id)
            if request.user.is_authenticated:
                cart = models.Cart.objects.filter(user=request.user).first()
            cart = models.Cart.objects.filter(query).first() if not cart else cart
            if not request.user and request.user.is_authenticated:
                cart.user = request.user
                cart.save(update_fields=["user"])
            if cart is None:
                cart = self.add_new_cart(request)
            if cart and not cart.is_cart_active():
                cart.set_cart_active()
        else:
            cart = self.add_new_cart(request)
        self.cart = cart
        self.promotion = Promotion(cart)

    @classmethod
    def add_new_cart(cls, request):
        if request.user.is_authenticated:
            cart = models.Cart.objects.create(user=request.user)
        else:
            cart = models.Cart.objects.create()
        request.session[CART_ID] = cart.id
        return cart

    def add_product(self, product):
        item = models.CartItem.objects.filter(cart=self.cart, product=product).first()
        if not item:
            models.CartItem.objects.create(cart=self.cart, product=product)

    def remove_product(self, product):
        item = models.CartItem.objects.filter(cart=self.cart, product=product).first()
        if item:
            item.delete()

    def update_product(self, product, quantity):
        item = models.CartItem.objects.filter(cart=self.cart, product=product).first()
        if item:
            if quantity == 0:
                item.delete()
            else:
                item.quantity = int(quantity)
                item.save()
        self.promotion.apply_promotions()
