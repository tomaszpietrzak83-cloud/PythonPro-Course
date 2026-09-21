from django.db import models


# TASK 10
class Dealer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


# TASK 10
class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to="car_photos/")
    owner_website = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    dealer = models.ForeignKey(
        Dealer, on_delete=models.CASCADE, related_name="cars"
    )

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
