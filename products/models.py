from django.db import models


class BaseForModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="If the entry is active or soft deleted")


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

    class Meta:
        get_latest_by = "created_at"
        ordering = ["-created_at"]
        verbose_name_plural = "Products"
        verbose_name = "Product"
        db_table = "product"
