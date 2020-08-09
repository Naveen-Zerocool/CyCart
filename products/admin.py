from django.contrib import admin
from .models import PromotionRule, Product


class PromotionRuleAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(PromotionRule, PromotionRuleAdmin)
