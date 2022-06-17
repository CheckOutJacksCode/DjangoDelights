from django.shortcuts import redirect
from multiprocessing import context, get_context
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import MenuItem, RecipeRequirement, Ingredient, Purchase
from .forms import MenuItemCreateForm, RecipeRequirementCreateForm, IngredientCreateForm, PurchaseCreateForm
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError

class HomeView(TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe_requirements"] = RecipeRequirement.objects.all()
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
    form_class = IngredientCreateForm
    template_name = "inventory/ingredient_create.html"

    #fields = ["name", "quantity", "unit", "unit_price"]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = [X for X in Ingredient.objects.all()]
        print(context["ingredients"])
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = request.POST['name']
            quantity = request.POST['quantity']
            unit = request.POST['unit']
            unit_price = request.POST['unit_price']
            for ingredient in Ingredient.objects.all():
                if ingredient.name == request.POST['name']:
                    print('INGREDIENT ALREADY EXISTS')
                    return redirect('/ingredient/list')
            new_ingredient = Ingredient.create_ingredient(name, quantity, unit, unit_price)
            new_ingredient.save()
            return redirect('/ingredient/list')

            #success_url = reverse_lazy('ingredientlist')
            #success_message = 'new ingredient added'

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
    form_class = MenuItemCreateForm
    success_url = reverse_lazy('menuitemlist')
    success_message = 'menu item update'

class MenuItemCreate(SuccessMessageMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menuitem_create.html"
    form_class = MenuItemCreateForm
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
        print(context["menu_items"])
        return context
        
    def post(self, request):
        menu_item_id = request.POST['menu_item']
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)
        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            print(required_ingredient.quantity)
            if required_ingredient.quantity < requirement.quantity:
                raise ValidationError(f"Not enough {required_ingredient} in the inventory!")
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