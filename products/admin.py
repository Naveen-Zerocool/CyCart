from django.contrib import admin
from .models import PromotionRule


class PromotionRuleAdmin(admin.ModelAdmin):
    pass


admin.site.register(PromotionRule, PromotionRuleAdmin)
