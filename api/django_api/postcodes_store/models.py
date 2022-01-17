from django.db import models


class Postcode(models.Model):
    key = models.CharField(max_length=50, db_index=True)
    ok = models.BooleanField()
    geocoded = models.CharField(max_length=50)
