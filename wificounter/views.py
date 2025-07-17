from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import Visit
from datetime import datetime
import calendar


def count_and_redirect(request):
    # Record the visit
    Visit.record_visit(request)

    # Redirect to your desired URL
    return redirect('https://twinfallspubliclibrary.org/')  # Change this to your target URL


def monthly_report(request, year=None, month=None):
    # Default to current month if no parameters
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    stats = Visit.get_monthly_stats(year, month)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(stats)

    return render(request, 'wificounter/report.html', {
        'stats': stats,  # Pass the stats to the template
        'all_months': [(i, calendar.month_name[i]) for i in range(1, 13)],
        'years': range(datetime.now().year - 5, datetime.now().year + 1),
        'default_year': datetime.now().year,
        'default_month': datetime.now().month,
    })


def all_reports(request):
    # Get all available years with data
    years_with_data = (
        Visit.objects.dates('timestamp', 'year')
        .values_list('timestamp__year', flat=True)
        .distinct()
    )

    reports = []
    for year in years_with_data:
        for month in range(1, 13):
            report = Visit.get_monthly_stats(year, month)
            if report['total_visits'] > 0:
                reports.append(report)

    return render(request, 'wificounter/all_reports.html', {
        'reports': sorted(reports, key=lambda x: (x['year'], x['month']), reverse=True)
    })