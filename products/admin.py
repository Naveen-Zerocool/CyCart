from django.contrib import admin
from .models import PromotionRule, Product


class PromotionRuleAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(PromotionRule, PromotionRuleAdmin)

admin.site.site_header = "CyKart Promotions and Products Admin"
admin.site.site_title = "CyKart Promotions and Products Admin Portal"
admin.site.index_title = "Welcome to CyKart Promotions and Products Admin Portal"
