from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.checkout"

    def ready(self) -> None:
        import modules.checkout.signals
