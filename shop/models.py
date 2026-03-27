from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='products/', null=True, blank=True)  # 👈 AJOUT

    def __str__(self):
        return self.name