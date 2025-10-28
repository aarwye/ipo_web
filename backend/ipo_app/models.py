from django.db import models

# Create your models here.

class IPO(models.Model):
    company_name = models.CharField(max_length=255)
    price_band = models.CharField(max_length=50)
    open_date = models.DateField()
    close_date = models.DateField()
    issue_size = models.CharField(max_length=50)
    issue_type = models.CharField(max_length=50)
    listing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    ipo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_gain = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.company_name