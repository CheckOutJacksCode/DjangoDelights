from django.shortcuts import redirect
from multiprocessing import get_context
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin


pets = [
  { "petname": "Fido", "animal_type": "dog"},
  { "petname": "Clementine", "animal_type": "cat"},
  { "petname": "Cleo", "animal_type": "cat"},
  { "petname": "Oreo", "animal_type": "dog"},
]

class HomeView(TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context

class IngredientList(ListView):
    model = Ingredient
    template_name: "inventory/ingredient_list.html"
    
class IngredientUpdate(UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_update.html"
    fields = ["name", "quantity", "unit", "unit_price"]
    success_url = reverse_lazy('ingredientlist')
    success_message = 'ingredient updated'

class IngredientCreate(CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_create.html"
    fields = ["name", "quantity", "unit", "unit_price"]
    success_url = reverse_lazy('ingredientlist')
    success_message = 'new ingredient added'

class IngredientDelete(DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete.html"
    success_url = reverse_lazy('ingredientlist')
    success_message = 'ingredient deleted '

class MenuItemList(ListView):
    model = MenuItem
    template_name: "inventory/menuitem_list.html"

class MenuItemUpdate(SuccessMessageMixin, UpdateView):
    model = MenuItem
    template_name = "inventory/menuitem_update.html"
    fields = ["title", "price"]
    success_url = reverse_lazy('menuitemlist')
    success_message = 'menu item update'

class MenuItemCreate(SuccessMessageMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menuitem_create.html"
    fields = ["title", "price"]
    success_url = reverse_lazy('menuitemlist')
    success_message = 'new menu item added'

class MenuItemDelete(SuccessMessageMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/menuitem_delete.html"
    success_url = reverse_lazy('menuitemlist')
    success_message = 'menu item deleted  '

class RecipeRequirementList(ListView):
    model = RecipeRequirement
    template_name: "inventory/reciperequirement_list.html"

class RecipeRequirementUpdate(SuccessMessageMixin, UpdateView):
    model = RecipeRequirement
    template_name = "inventory/reciperequirement_update.html"
    fields = ["menu_item", "ingredient", "quantity"]
    success_url = reverse_lazy('reciperequirementlist')
    success_message = 'recipe requirement update'

class RecipeRequirementCreate(SuccessMessageMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/reciperequirement_create.html"
    fields = ["menu_item", "ingredient", "quantity"]
    success_url = reverse_lazy('reciperequirementlist')
    success_message = 'new recipe requirement added'

class RecipeRequirementDelete(SuccessMessageMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory/reciperequirement_delete.html"
    success_url = reverse_lazy('reciperequirementlist')
    success_message = 'recipe requirement deleted'

class PurchaseList(ListView):
    model = Purchase
    template_name = "inventory/purchase_list.html"

class PurchaseUpdate(SuccessMessageMixin, UpdateView):
    model = Purchase
    template_name = "inventory/purchase_update.html"
    fields = ["menu_item", "timestamp"]
    success_url = reverse_lazy('purchaselist')
    success_message = 'purchase updated'

class PurchaseCreate(SuccessMessageMixin, CreateView):
    model = Purchase
    template_name = "inventory/purchase_create.html"
    fields = ["menu_item", "timestamp"]
    #success_url = reverse_lazy('purchaselist')
    #success_message = 'new purchase added'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context
        
    def post(self, request):
        print(request)
        menu_item_id = request.POST['menu_item']
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)
        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            print(required_ingredient.quantity)
            required_ingredient.quantity -= requirement.quantity
            print(required_ingredient.quantity)
            required_ingredient.save()
        purchase.save()
        return redirect('/purchase/list')




class PurchaseDelete(SuccessMessageMixin, DeleteView):
    model = Purchase
    template_name = "inventory/purchase_delete.html"
    success_url = reverse_lazy('purchaselist')
    success_message = 'purchase deleted'