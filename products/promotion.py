from datetime import datetime

import pytz

from products.models import PromotionRule, CartItem, Product


class Promotion:

    def __init__(self, cart):
        self.active_promotions = PromotionRule.objects.filter(disable=False, is_active=True,
                                                              start_from__lte=datetime.now(tz=pytz.UTC))
        self.cart = cart

    def apply_cart_promotions(self):
        rules = self.active_promotions.filter(promotion_for=PromotionRule.PROMOTION_FOR_CART)
        initial_discount = self.cart.discount
        if rules.exists():
            for promotion_rule in rules:
                if promotion_rule.discount_on == PromotionRule.DISCOUNT_ON_CART_TOTAL:
                    if self.cart.price >= promotion_rule.discount_condition_value:
                        if promotion_rule.promotion_type == PromotionRule.PROMOTION_TYPE_FIXED_AMOUNT:
                            self.cart.discount = promotion_rule.discount_price if promotion_rule.discount_price <= self.cart.price else 0
                        if promotion_rule.promotion_type == PromotionRule.PROMOTION_TYPE_DISCOUNT_PERCENTAGE:
                            self.cart.discount = (self.cart.price * promotion_rule.discount_percentage) / 100
                    else:
                        self.cart.discount = 0
        if initial_discount != self.cart.discount:
            self.cart.save()

    def apply_cart_item_promotions(self):
        product_items = CartItem.get_all_items_on_cart(cart=self.cart)
        rules = self.active_promotions.filter(promotion_for=PromotionRule.PROMOTION_FOR_PRODUCT,
                                              products__in=product_items.values_list('product_id', flat=True))
        if rules.exists():
            for product in product_items:
                initial_discount = product.discount
                product_promotion_rule = rules.filter(products__in=[product.product])
                for promotion_rule in product_promotion_rule:
                    if promotion_rule.discount_on == PromotionRule.DISCOUNT_ON_PRODUCT_COUNT:
                        if product.quantity >= promotion_rule.discount_condition_value:
                            if promotion_rule.promotion_type == PromotionRule.PROMOTION_TYPE_FIXED_AMOUNT:
                                product.discount = promotion_rule.discount_price
                            if promotion_rule.promotion_type == PromotionRule.PROMOTION_TYPE_DISCOUNT_PERCENTAGE:
                                product.discount = (product.total_price * promotion_rule.discount_percentage) / 100
                        else:
                            product.discount = 0
                    if initial_discount != product.discount:
                        product.save()

        if not product_items and self.cart.price > 0:
            self.cart.price = 0
            self.cart.save()

    def apply_promotions(self):
        self.apply_cart_item_promotions()
        self.cart.update_price()
        self.apply_cart_promotions()
