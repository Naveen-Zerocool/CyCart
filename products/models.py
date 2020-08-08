from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class BaseForModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="If the entry is active or soft deleted")

    class Meta:
        abstract = True


class ActiveProductsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductsManager, self).get_queryset().filter(is_active=True)


class Product(BaseForModels):
    """
    This is model class for product
    """
    title = models.CharField(max_length=64, help_text="Title of the product")
    description = models.TextField(help_text="Description of the product")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Price of the product")
    image = models.URLField(help_text="Image for the product", null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True, help_text="Stock available for the product")

    objects = ActiveProductsManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.title

    @staticmethod
    def get_product_based_on_id(product_id):
        return Product.objects.filter(pk=product_id).first()

    class Meta:
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        verbose_name_plural = "Products"
        verbose_name = "Product"
        db_table = "product"


class Cart(BaseForModels):
    """
    This is model class for Cart/ Basket
    """
    user = models.OneToOneField(User, related_name="shopping_cart", null=True, blank=True,
                                help_text="If logged in user, then Cart will be saved against this User",
                                on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(default=0, help_text="Price of all products on cart")
    discount = models.PositiveSmallIntegerField(default=0, help_text="Discount amount on cart")

    def is_cart_active(self):
        """
        Used to check if Cart is soft deleted or active
        """
        return self.is_active

    def set_cart_active(self):
        """
        Used to set cart as active if deleted
        """
        if not self.is_cart_active():
            self.is_active = True
            self.save(update_fields=["is_active"])

    class Meta:
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        verbose_name_plural = "Carts"
        verbose_name = "Cart"
        db_table = "cart"


class CartItem(BaseForModels):
    """
    This is model class for each cart item on the shopping cart/ basket
    """
    cart = models.ForeignKey(Cart, related_name="cart_item", help_text="To which cart this item is associated with",
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_product", help_text="Associated product on the cart",
                                on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)],
                                                help_text="Quantity of the item on cart")

    def __str__(self):
        return self.product.title

    @staticmethod
    def get_all_items_on_cart(cart):
        """
        Used to return all the items under a cart by passing cart
        """
        return CartItem.objects.filter(cart=cart)

    class Meta:
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        verbose_name_plural = "Items"
        verbose_name = "Item"
        db_table = "cart_item"
