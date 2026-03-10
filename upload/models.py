from django.db import models

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


STATUS_CHOICE = (
    ('draft', 'Draft'),
    ('approved', 'Approved'),
)


class Product(Timestamp):
    product_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

    def __str__(self):
        return self.name


