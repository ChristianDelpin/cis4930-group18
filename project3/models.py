from django.db import models

class Country(models.Model):
    cca2 = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'currency_list'

    def __str__(self):
        return self.name