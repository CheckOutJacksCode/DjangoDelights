from datetime import datetime
from django.db import models

# Create your models here.
class Ingredient (models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=100)
    unit_price = models.FloatField()
    
    def create_ingredient (name, quantity, unit, unit_price):
        ingredient = Ingredient.objects.create(name=name, quantity=quantity, unit=unit, unit_price=unit_price)
        return ingredient
    
    def __str__(self):
        return self.name

class MenuItem (models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    def __str__(self):
        return self.title

    def available(self):
        if all(X.enough() for X in self.reciperequirement_set.all()) == False:
            print('This menu item is not available')
        print(all(X.enough() for X in self.reciperequirement_set.all()))
        return all(X.enough() for X in self.reciperequirement_set.all())

class RecipeRequirement (models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def enough(self):
        return self.quantity <= self.ingredient.quantity

class Purchase (models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.menu_item.title) + ' ' + str(self.timestamp)

