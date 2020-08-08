from rest_framework import serializers

from products.models import Product, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    @staticmethod
    def get_items(obj):
        return CartItemSerializer(CartItem.get_all_items_on_cart(obj), many=True).data

    class Meta:
        model = Cart
        exclude = ["is_active", "user", "created_at", "modified_at"]


class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    @staticmethod
    def get_title(obj):
        return obj.product.title

    @staticmethod
    def get_description(obj):
        return obj.product.description

    @staticmethod
    def get_price(obj):
        return obj.product.price

    @staticmethod
    def get_image(obj):
        return obj.product.image

    class Meta:
        model = CartItem
        fields = ["pk", "title", "description", "price", "image", "quantity"]
