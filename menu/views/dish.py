# import django.shortcuts as dshortcuts
# import django.urls as durls
# import django.http as dhttp
# import django.forms as dforms
# import django.contrib.messages as dmessages
#
# from ..forms import DishForm, Dish2IngredientForm
# from ..models import Dish, Dish2Ingredient, Ingredient
#
# def dish_get(request):
# 	dish_form = DishForm()
# 	dish2ingredient_formset = dforms.formsets.formset_factory(Dish2IngredientForm)()
# 	dish_set = Dish.objects.all()
#
# 	context = {
# 		'dish_form' : dish_form,
# 		'dish2ingredient_formset' : dish2ingredient_formset,
# 		'dish_set' : dish_set
# 	}
# 	return dshortcuts.render(request, 'menu/dish.html', context)
#
# def dish_post(request):
# 	dish_form = DishForm(request.POST)
# 	dish2ingredient_formset = dforms.formsets.formset_factory(Dish2IngredientForm)(request.POST)
#
# 	if not dish_form.is_valid() or not dish2ingredient_formset.is_valid():
# 		dmessages.error(request, "输入错误")
# 		return dhttp.HttpResponseRedirect(durls.reverse('menu:dish'))
#
# 	ingredient_set = set()
# 	for dish2ingredient_form in dish2ingredient_formset:
# 		try:
# 			ingredient_name = dish2ingredient_form.cleaned_data.get('ingredient_name')
# 			if ingredient_name in ingredient_set:
# 				dmessages.error(request, "配料%s输入了两次，请重新输入" % ingredient_name)
# 				return dhttp.HttpResponseRedirect(durls.reverse('menu:dish'))
# 			else:
# 				ingredient_set.add(ingredient_name)
# 			ingredient = Ingredient.objects.get(name = ingredient_name)
# 		except Ingredient.DoesNotExist:
# 			dmessages.error(request, "配料%s不存在，请先添加配料." % (ingredient_name))
# 			return dhttp.HttpResponseRedirect(durls.reverse('menu:dish'))
# 		except Ingredient.MultipleObjectsReturned:
# 			dmessages.error(request, "记录中存在多个关于配料%s的信息" % (ingredient_name))
# 			return dhttp.HttpResponseRedirect(durls.reverse('menu:dish'))
#
# 	# Collects all ingredients and quantities
# 	dish_name = dish_form.cleaned_data.get('dish_name')
# 	Dish.objects.filter(name = dish_name).delete()
# 	dish = Dish.objects.create(name = dish_name)
#
# 	for dish2ingredient_form in dish2ingredient_formset:
# 		ingredient_name = dish2ingredient_form.cleaned_data.get('ingredient_name')
# 		ingredient = Ingredient.objects.get(name = ingredient_name)
# 		quantity = dish2ingredient_form.cleaned_data.get('quantity')
# 		Dish2Ingredient.objects.create(dish = dish, ingredient = ingredient, quantity = quantity)
#
# 	dmessages.success(request, "成功添加菜品!")
# 	return dhttp.HttpResponseRedirect(durls.reverse('menu:dish'))
#
#
# def dish(request):
# 	if request.method == 'POST':
# 		return dish_post(request)
# 	else:
# 		return dish_get(request)