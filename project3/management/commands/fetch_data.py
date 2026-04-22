"""
Django management command to fetch countries and currencies data from REST Countries API.
Usage: python manage.py fetch_data
"""
import requests
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.timezone import now

from project3.models import Country, Currency

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetch countries and currencies data from REST Countries API and save to database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=50,
            help="Number of records to process per API call (default: 50)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Print detailed output",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        verbose = options["verbose"]

        try:
            self.stdout.write(
                self.style.SUCCESS("Starting data fetch from REST Countries API...")
            )

            # Step 1: Fetch currencies
            currencies_count = self._fetch_currencies(verbose)
            self.stdout.write(
                self.style.SUCCESS(f"✓ Fetched/updated {currencies_count} currencies")
            )

            # Step 2: Fetch countries
            countries_count = self._fetch_countries(batch_size, verbose)
            self.stdout.write(
                self.style.SUCCESS(f"✓ Fetched/updated {countries_count} countries")
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Data fetch completed successfully!\n"
                    f"  - Currencies: {currencies_count}\n"
                    f"  - Countries: {countries_count}"
                )
            )

        except requests.exceptions.RequestException as e:
            raise CommandError(f"API request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during data fetch: {e}")
            raise CommandError(f"Unexpected error: {e}")

    def _fetch_currencies(self, verbose=False):
        """
        Fetch all unique currencies from REST Countries API.

        Returns:
            int: Number of currencies fetched/updated
        """
        try:
            if verbose:
                self.stdout.write("Fetching currency list...")

            url = "https://restcountries.com/v3.1/all"
            params = {"fields": "currencies"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract unique currencies
            currencies_dict = {}
            for country_data in data:
                currencies = country_data.get("currencies", {})
                for code, info in currencies.items():
                    if code not in currencies_dict:
                        currencies_dict[code] = {
                            "name": info.get("name", "Unknown"),
                            "symbol": info.get("symbol", ""),
                        }

            # Save to database
            count = 0
            with transaction.atomic():
                for code, info in currencies_dict.items():
                    currency, created = Currency.objects.get_or_create(
                        code=code,
                        defaults={
                            "name": info["name"],
                            "symbol": info["symbol"],
                        },
                    )
                    if created and verbose:
                        self.stdout.write(f"  Created currency: {code} ({info['name']})")
                    count += 1

            return count

        except requests.exceptions.Timeout:
            raise CommandError("Request timed out while fetching currencies")
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Failed to fetch currencies: {e}")

    def _fetch_countries(self, batch_size=50, verbose=False):
        """
        Fetch all countries from REST Countries API.
        Handles pagination by slicing the full response.

        Args:
            batch_size (int): Number of countries to process per call
            verbose (bool): Print detailed output

        Returns:
            int: Number of countries fetched/updated
        """
        try:
            if verbose:
                self.stdout.write("Fetching countries list...")

            url = "https://restcountries.com/v3.1/all"
            params = {"fields": "cca2,name,population,region,capital,currencies"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            all_countries = response.json()
            total_countries = len(all_countries)

            if verbose:
                self.stdout.write(f"Retrieved {total_countries} countries from API")

            count = 0
            errors = 0

            with transaction.atomic():
                for i, country_data in enumerate(all_countries, 1):
                    try:
                        cca2 = country_data.get("cca2", "").upper()
                        name = country_data.get("name", {}).get("common", "Unknown")

                        if not cca2 or not name:
                            if verbose:
                                self.stdout.write(
                                    self.style.WARNING(f"Skipping country with missing cca2 or name")
                                )
                            continue

                        country, created = Country.objects.get_or_create(
                            cca2=cca2,
                            defaults={"name": name},
                        )

                        if not created:
                            # Update name if changed
                            country.name = name
                            country.save()

                        if created and verbose:
                            self.stdout.write(f"  [{i}/{total_countries}] Created: {cca2} - {name}")
                        elif verbose and i % batch_size == 0:
                            self.stdout.write(f"  [{i}/{total_countries}] Processing...")

                        count += 1

                    except Exception as e:
                        logger.error(f"Error processing country {country_data}: {e}")
                        errors += 1
                        continue

            if errors > 0:
                self.stdout.write(
                    self.style.WARNING(f"Completed with {errors} errors")
                )

            return count

        except requests.exceptions.Timeout:
            raise CommandError("Request timed out while fetching countries")
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Failed to fetch countries: {e}")
