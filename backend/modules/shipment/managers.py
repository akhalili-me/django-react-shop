from django.db import models


class BillingAddressManager(models.Manager):
    def create_bill_addr_from_user_addr(self, user_address_uuid):
        from .models import UserAddress, BillingAddress

        user_address = UserAddress.objects.get(uuid=user_address_uuid)
        bill_addr_kwargs = {
            "state": user_address.state,
            "city": user_address.city,
            "phone": user_address.phone,
            "postal_code": user_address.postal_code,
            "street_address": user_address.street_address,
            "house_number": user_address.house_number,
        }
        return BillingAddress.objects.create(**bill_addr_kwargs)
