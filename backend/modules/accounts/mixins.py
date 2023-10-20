from .models import Ban
from django.utils import timezone
from .api_exceptions import UserBannedForThisActionException


class BanCheckMixin:
    """
    Mixin to check if a user is banned for a specific action type.
    """

    def check_ban(self, user):
        now = timezone.now()
        is_ban = Ban.objects.filter(
            user=user, ban_type=self.ban_type, banned_until__gte=now
        ).exists()

        return is_ban

    def create(self, request, *args, **kwargs):
        is_ban = self.check_ban(request.user)

        if is_ban:
            raise UserBannedForThisActionException(self.ban_type)

        return super().create(request, *args, **kwargs)
