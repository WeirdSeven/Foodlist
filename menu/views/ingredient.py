# import django.shortcuts as dshortcuts
# import django.urls as durls
# import django.contrib.messages as dmessages
# import django.http as dhttp
#
# from ..forms import IngredientForm
# from ..models import Ingredient
#
# def ingredient(request):
# 	if request.method == 'POST':
# 		ingredient_form = IngredientForm(request.POST)
# 		if ingredient_form.is_valid():
# 			ingredient_name = ingredient_form.cleaned_data.get('name')
# 			price = ingredient_form.cleaned_data.get('price')
# 			ratio = ingredient_form.cleaned_data.get('ratio')
#
# 			Ingredient.objects.filter(name = ingredient_name).delete()
# 			Ingredient.objects.create(name = ingredient_name, price = price, ratio = ratio)
# 		else:
# 			dmessages.error(request, ingredient_form.errors)
#
# 		return dhttp.HttpResponseRedirect(durls.reverse('menu:ingredient'))
# 	else:
# 		form = IngredientForm()
# 		ingredient_set = Ingredient.objects.all()
# 		context = {
# 			'ingredient_set' : ingredient_set,
# 			'form' : form
# 		}
# 		return dshortcuts.render(request, 'menu/ingredient.html', context)