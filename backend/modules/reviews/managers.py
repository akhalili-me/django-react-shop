from django.db import models
from datetime import timedelta
from django.utils import timezone

class ReportManager(models.Manager):
    def get_user_today_reports_count(self, user):
        from .models import Report

        today = timezone.now()
        return Report.objects.filter(user=user, created_at__date=today).count()

    def get_user_past_seven_days_reports_count(self, user):
        from .models import Report

        seven_days_ago = timezone.now() - timedelta(days=7)
        return Report.objects.filter(user=user, created_at__gte=seven_days_ago).count()
