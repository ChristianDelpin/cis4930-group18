from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db import connections
from .models import Country, Currency

def home(request):
    return render(request, 'core/home.html')

def project1(request):
    return render(request, 'core/project1.html')

class CurrencyListView(ListView):
    model = Currency
    template_name = 'core/currency_list.html'
    context_object_name = 'currency_list'

    def get_queryset(self):
        allowed_sort_fields = {'code', 'symbol', 'name'}
        sort = self.request.GET.get('sort', 'code').lower()
        direction = self.request.GET.get('dir', 'asc').lower()

        if sort not in allowed_sort_fields:
            sort = 'code'
        if direction not in {'asc', 'desc'}:
            direction = 'asc'

        self.current_sort = sort
        self.current_dir = direction

        order_field = sort if direction == 'asc' else f'-{sort}'
        return Currency.objects.using('currencies').all().order_by(order_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = getattr(self, 'current_sort', 'code')
        context['current_dir'] = getattr(self, 'current_dir', 'asc')
        return context



class CountryListView(ListView):
    model = Country
    template_name = 'core/country_list.html'
    context_object_name = 'country_list'

    def get_queryset(self):
        return Country.objects.using('countries').all()


def currency_countries(request, code):
    currency_code = code.upper()

    with connections['currencies'].cursor() as cursor:
        cursor.execute(
            "SELECT code, name, symbol FROM currency_list WHERE code = %s",
            [currency_code],
        )
        currency_row = cursor.fetchone()

        cursor.execute(
            """
            SELECT cca2
            FROM country_currency_junction
            WHERE currency_code = %s
            ORDER BY cca2
            """,
            [currency_code],
        )
        country_codes = [row[0] for row in cursor.fetchall()]

    context = {
        'currency': currency_row,
        'currency_code': currency_code,
        'country_codes': country_codes,
    }
    return render(request, 'core/currency_countries.html', context)