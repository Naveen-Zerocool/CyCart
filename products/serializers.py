from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from products.models import Product, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    price = serializers.DecimalField(source="product.price", max_digits=6, decimal_places=2)
    image = serializers.URLField(source="product.image")

    class Meta:
        model = CartItem
        fields = ["pk", "product", "title", "description", "price", "image", "quantity", "total_price", "discount",
                  "final_price"]


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    @staticmethod
    @swagger_serializer_method(serializer_or_field=CartItemSerializer(many=True))
    def get_items(obj):
        return CartItemSerializer(CartItem.get_all_items_on_cart(obj), many=True).data

    @staticmethod
    def get_final_price(obj):
        return obj.price - obj.discount

    class Meta:
        model = Cart
        exclude = ["is_active", "user", "created_at", "modified_at"]


class CartAddSerializer(serializers.Serializer):
    """
    Serializer to represent in docs
    """
    product_id = serializers.IntegerField()

    class Meta:
        fields = ["product_id"]


class CartEditSerializer(serializers.Serializer):
    """
    Serializer to represent in docs
    """
    product_id = serializers.IntegerField()
    action = serializers.CharField(default="update/remove")
    quantity = serializers.IntegerField()

    class Meta:
        fields = ["product_id", "action", "quantity"]
