from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.products"

    def ready(self):
        import modules.products.signals
