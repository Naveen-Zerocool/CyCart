from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart
from .constants import ACTION_UPDATE, ACTION_REMOVE
from .serializers import ProductSerializer, CartSerializer, CartAddSerializer, CartEditSerializer
from .models import Product
from rest_framework.authentication import SessionAuthentication


class ProductsView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class CartViews(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    @swagger_auto_schema(responses={200: CartSerializer})
    def get(self, request):
        """
        Get details of cart
        """
        cart = Cart(request)
        return Response(CartSerializer(cart.cart).data)

    @swagger_auto_schema(responses={201: CartSerializer}, request_body=CartAddSerializer)
    def post(self, request):
        """
        Add a product to Cart
        """
        cart = Cart(request)
        product = None
        if request.data.get('product_id'):
            product = Product.get_product_based_on_id(request.data.get('product_id'))
        if product:
            cart.add_product(product)
        return Response(CartSerializer(cart.cart).data)

    @swagger_auto_schema(responses={200: CartSerializer}, request_body=CartEditSerializer)
    def put(self, request):
        """
        Update or remove a product on Cart
        """
        cart = Cart(request)
        product = None
        action_to_do = request.data.get('action')
        quantity = request.data.get('quantity')
        if request.data.get('product_id'):
            product = Product.get_product_based_on_id(request.data.get('product_id'))
        if product and action_to_do:
            if action_to_do == ACTION_REMOVE:
                cart.remove_product(product)
            if action_to_do == ACTION_UPDATE:
                cart.update_product(product, quantity)
        return Response(CartSerializer(cart.cart).data)
