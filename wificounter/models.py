from django.db import models
from django.utils import timezone
from django.db.models import Count, Sum
import calendar
from datetime import date


# Create your models here.
class Visit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    @classmethod
    def record_visit(cls, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # Gets the first IP in the list
        else:
            ip = request.META.get('REMOTE_ADDR')

        return cls.objects.create(
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
        )

    @classmethod
    def get_monthly_stats(cls, year=None, month=None):
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month

        print(f"Querying for year: {year}, month: {month}")  # Debug line

        # Get first and last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        print(f"Date range: {start_date} to {end_date}")  # Debug line

        # Query for daily counts
        daily_counts = (
            cls.objects.filter(
                timestamp__date__gte=start_date,
                timestamp__date__lte=end_date
            )
            .extra({'day': "date(timestamp)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Convert the queryset to list to evaluate it now
        daily_counts_list = list(daily_counts)
        print(f"Found {len(daily_counts_list)} days with data")  # Debug line

        # Get total for the month
        total = cls.objects.filter(
            timestamp__year=year,
            timestamp__month=month
        ).count()

        print(f"Total visits: {total}")  # Debug line

        # Get unique IPs for the month
        unique_ips = (
            cls.objects.filter(
                timestamp__year=year,
                timestamp__month=month
            )
            .values('ip_address')
            .distinct()
            .count()
        )

        print(f"Unique visitors: {unique_ips}")  # Debug line

        return {
            'year': year,
            'month': month,
            'month_name': calendar.month_name[month],
            'total_visits': total,
            'unique_visitors': unique_ips,
            'daily_breakdown': daily_counts_list,
        }