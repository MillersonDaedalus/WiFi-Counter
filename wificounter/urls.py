from django.urls import path
from .views import count_and_redirect, monthly_report, all_reports

urlpatterns = [
    path('', count_and_redirect, name='count-and-redirect'),
    path('stats/monthly/', monthly_report, name='monthly-report'),
    path('stats/monthly/<int:year>/<int:month>/', monthly_report, name='monthly-report-detail'),
    path('stats/all/', all_reports, name='all-reports'),
    ]