from django.core.management.base import BaseCommand
from wificounter.models import Visit
from datetime import datetime, timedelta
import csv


class Command(BaseCommand):
    help = 'Generates a CSV report of monthly statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='Year for the report (default: current year)',
        )
        parser.add_argument(
            '--month',
            type=int,
            help='Month for the report (default: previous month)',
        )
        parser.add_argument(
            '--output',
            type=str,
            default='monthly_report.csv',
            help='Output file path (default: monthly_report.csv)',
        )

    def handle(self, *args, **options):
        now = datetime.now()
        year = options['year'] or now.year
        month = options['month'] or (now.month - 1 if now.month > 1 else 12)

        if month == 0:  # Handle January case
            month = 12
            year -= 1

        stats = Visit.get_monthly_stats(year, month)

        with open(options['output'], 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Month', 'Year', 'Total Visits', 'Unique Visitors'])
            writer.writerow([
                stats['month_name'],
                stats['year'],
                stats['total_visits'],
                stats['unique_visitors']
            ])

            writer.writerow([])  # Empty row
            writer.writerow(['Date', 'Visits'])  # Daily breakdown header

            for day in stats['daily_breakdown']:
                writer.writerow([day['day'], day['count']])

        self.stdout.write(self.style.SUCCESS(
            f'Successfully generated report for {stats["month_name"]} {stats["year"]}'
            f' at {options["output"]}'
        ))