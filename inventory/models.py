from django.db import models

# Create your models here.
class Ingredient (models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=100)
    unit_price = models.FloatField()

class MenuItem (models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()

class RecipeRequirement (models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Purchase (models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
