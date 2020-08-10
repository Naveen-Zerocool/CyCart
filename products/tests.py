import json
from datetime import datetime

import pytz
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .models import Product, Cart, PromotionRule
from .serializers import ProductSerializer, CartSerializer


# Test cases for models
# Below is test case for products model

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(title="Test Product", description="Test Description", price=100)

    def test_getting_project_based_on_product_id(self):
        self.assertEqual(self.product, Product.get_product_based_on_id(self.product.pk))


# Below is test case for cart model
class CartModelTest(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create()

    def change_active_cart_status(self, status):
        self.cart.is_active = status
        self.cart.save()

    def test_is_cart_active(self):
        self.assertEqual(self.cart.is_active, True)
        self.change_active_cart_status(False)
        self.assertEqual(self.cart.is_active, False)
        self.change_active_cart_status(True)

    def test_set_cart_active(self):
        self.change_active_cart_status(False)
        self.assertEqual(self.cart.is_active, False)
        self.cart.set_cart_active()
        self.assertEqual(self.cart.is_active, True)


# Test cases for APIs
# Below is test case for Products API

class ProductsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_data = {
            "title": "This is a test Product title",
            "description": "This is a test Product description",
            "price": 100.00
        }

    def create_a_product_object(self):
        Product.objects.create(**self.post_data)

    def test_adding_a_product(self):
        response = self.client.post(reverse('product-list'), data=json.dumps(self.post_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        serializer = ProductSerializer(Product.objects.last())
        self.assertEqual(response.data, serializer.data)

    def test_getting_all_products(self):
        self.create_a_product_object()
        self.create_a_product_object()
        response = self.client.get(reverse('product-list'))
        serializer = ProductSerializer(Product.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_get_one_product(self):
        self.create_a_product_object()
        serializer = ProductSerializer(Product.objects.last())
        response = self.client.get(reverse('product-detail', kwargs={"pk": Product.objects.last().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_updating_a_product(self):
        self.create_a_product_object()
        serializer = ProductSerializer(Product.objects.last())
        response = self.client.get(reverse('product-detail', kwargs={"pk": Product.objects.last().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        response = self.client.patch(reverse('product-detail', kwargs={"pk": Product.objects.last().pk}),
                                     data=json.dumps({"price": 50.0}), content_type='application/json')
        serializer = ProductSerializer(Product.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_deleting_a_product(self):
        self.create_a_product_object()
        self.assertEqual(Product.objects.last().is_active, True)
        response = self.client.delete(reverse('product-detail', kwargs={"pk": Product.objects.last().pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.all_objects.last().is_active, False)


# Below is test case for Cart API
class CartAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_a_product(self):
        Product.objects.create(title="This is a test Product title", description="This is a test Product description",
                               price=100.00)

    def test_getting_a_cart(self):
        response = self.client.get(reverse('user_cart'))
        serializer = CartSerializer(Cart.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_adding_a_product_to_cart(self):
        self.create_a_product()
        response = self.client.post(reverse('user_cart'), data=json.dumps({"product_id": Product.objects.last().pk}),
                                    content_type='application/json')
        serializer = CartSerializer(Cart.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_updating_a_product_on_cart(self):
        self.test_adding_a_product_to_cart()
        response = self.client.put(reverse('user_cart'), data=json.dumps({"product_id": Product.objects.last().pk,
                                                                          "action": "update", "quantity": 10}),
                                   content_type='application/json')
        serializer = CartSerializer(Cart.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_removing_a_product_from_cart(self):
        self.test_adding_a_product_to_cart()
        response = self.client.put(reverse('user_cart'), data=json.dumps({"product_id": Product.objects.last().pk,
                                                                          "action": "remove"}),
                                   content_type='application/json')
        serializer = CartSerializer(Cart.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)


# Tests for added promotion logic

class PromotionLogicTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.productA = {
            "title": "This is a test Product A",
            "description": "This is a test Product description for A",
            "price": 30.00
        }
        self.promotion_discount_cart_fixed_amount = {
            'start_from': datetime.now(tz=pytz.UTC), 'discount_percentage': None, 'disable': False,
            'promotion_for': 'cart', 'promotion_type': 'fixed_discount_amount', 'discount_price': '20.00',
            'name': 'If Cart Total is above 150, get 20 offer', 'discount_condition_value': 150, 'end_by': None,
            'is_active': True, 'discount_on': 'total_value'
        }
        self.promotion_discount_cart_fixed_percentage = {
            'start_from': datetime.now(tz=pytz.UTC), 'discount_percentage': 50, 'disable': False,
            'promotion_for': 'cart', 'promotion_type': 'discount_percentage', 'discount_price': None,
            'name': 'If Cart Total is above 150, get 50% offer', 'discount_condition_value': 150, 'end_by': None,
            'is_active': True, 'discount_on': 'total_value'
        }
        self.promotion_discount_product_fixed_amount = {
            'start_from': datetime.now(tz=pytz.UTC), 'discount_percentage': None, 'disable': False,
            'promotion_for': 'product', 'promotion_type': 'fixed_discount_amount', 'discount_price': '40.00',
            'name': 'Buy 3 A, get fixed 40 discount', 'discount_condition_value': 3, 'end_by': None,
            'is_active': True, 'discount_on': 'product_counts'
        }
        self.promotion_discount_product_percentage_amount = {
            'start_from': datetime.now(tz=pytz.UTC), 'discount_percentage': 50, 'disable': False,
            'promotion_for': 'product', 'promotion_type': 'discount_percentage', 'discount_price': None,
            'name': 'Buy 3 A or more, get fixed 50% discount', 'discount_condition_value': 3, 'end_by': None,
            'is_active': True, 'discount_on': 'product_counts'
        }
        self.promotion_discount_product_flat_amount = {
            'start_from': datetime.now(tz=pytz.UTC), 'discount_percentage': None, 'disable': False,
            'promotion_for': 'product', 'promotion_type': 'product_fixed_price', 'discount_price': 75,
            'name': 'Buy 3 A for Rs 75', 'discount_condition_value': 3, 'end_by': None,
            'is_active': True, 'discount_on': 'product_counts'
        }

    def create_required_data_cart(self, promotion_rule):
        Product.objects.create(**self.productA)
        PromotionRule.objects.create(**promotion_rule)

    def create_required_data_product(self, promotion_rule):
        Product.objects.create(**self.productA)
        promotion_rule = PromotionRule.objects.create(**promotion_rule)
        promotion_rule.products.add(Product.objects.get(title=self.productA["title"]).pk)

    def add_a_product_to_cart(self):
        response = self.client.get(reverse('user_cart'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('user_cart'),
                                    data=json.dumps(
                                        {"product_id": Product.objects.get(title=self.productA["title"]).pk}
                                    ),
                                    content_type='application/json')
        serializer = CartSerializer(Cart.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(float(response.data["items"][0]["price"]), self.productA["price"])
        self.assertEqual(response.data["items"][0]["discount"], '0.00')
        self.assertEqual(float(response.data["items"][0]["total_price"]), self.productA["price"])

    def update_product_quantity(self):
        response = self.client.put(reverse('user_cart'),
                                   data=json.dumps(
                                       {"product_id": Product.objects.get(title=self.productA["title"]).pk,
                                        "action": "update", "quantity": 10}
                                   ),
                                   content_type='application/json')
        serializer = CartSerializer(Cart.objects.last())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
        return response

    def check_product_discounts(self, response, total_price, discount, price):
        self.assertEqual(response.data["items"][0]["total_price"], total_price)
        self.assertEqual(response.data["items"][0]["discount"], discount)
        self.assertEqual(response.data["price"], price)

    def check_cart_discounts(self, response, price, discount, final_price):
        self.assertEqual(response.data["discount"], discount)
        self.assertEqual(response.data["price"], price)
        self.assertEqual(int(response.data["final_price"]), final_price)

    def test_total_cart_value_fixed_amount_discount(self):
        """
        If cart total is more than 150 get flat 20 rs discount
        """
        self.create_required_data_cart(self.promotion_discount_cart_fixed_amount)
        self.add_a_product_to_cart()
        response = self.update_product_quantity()
        self.check_cart_discounts(response=response, price='300.00', discount='20.00', final_price=280)

    def test_total_cart_value_fixed_percentage_discount(self):
        """
        If cart total is more than 150 get flat 50 % discount
        """
        self.create_required_data_cart(self.promotion_discount_cart_fixed_percentage)
        self.add_a_product_to_cart()
        response = self.update_product_quantity()
        self.check_cart_discounts(response=response, price='300.00', discount='150.00', final_price=150)

    def test_if_certain_product_count_fixed_amount_discount(self):
        """
        Buy more than 3 of product A and get flat 40 rs discount
        """
        self.create_required_data_product(self.promotion_discount_product_fixed_amount)
        self.add_a_product_to_cart()
        response = self.update_product_quantity()
        self.check_product_discounts(response=response, total_price='300.00', discount='40.00', price='260.00')

    def test_if_certain_product_count_fixed_percentage_discount(self):
        """
        Buy more than 3 of product A and get flat 50 % discount
        """
        self.create_required_data_product(self.promotion_discount_product_percentage_amount)
        self.add_a_product_to_cart()
        response = self.update_product_quantity()
        self.check_product_discounts(response=response, total_price='300.00', discount='150.00', price='150.00')

    def test_if_certain_product_count_flat_amount_discount(self):
        """
        Buy 3 of product A for 75 Rs
        """
        self.create_required_data_product(self.promotion_discount_product_flat_amount)
        self.add_a_product_to_cart()
        response = self.update_product_quantity()
        self.check_product_discounts(response=response, total_price='300.00', discount='45.00', price='255.00')
