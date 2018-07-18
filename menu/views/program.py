import django.shortcuts as dshortcuts
import django.urls as durls
import django.http as dhttp
import django.forms as dforms
import django.contrib.messages as dmessages


from ..models import Program, Program2Dish, Dish
from ..forms import ProgramForm, Program2DishForm


def program_get(request):
	program_form = ProgramForm()
	program2dish_formset = dforms.formsets.formset_factory(Program2DishForm)()

	program_set = Program.objects.all()

	context = {
		'program_form' : program_form,
		'program2dish_formset' : program2dish_formset,
		'program_set' : program_set
	}
	return dshortcuts.render(request, 'menu/program.html', context)

def program_post(request):
	program_form = ProgramForm(request.POST)
	program2dish_formset = dforms.formsets.formset_factory(Program2DishForm)(request.POST)

	if not program_form.is_valid() or not program2dish_formset.is_valid():
		return dhttp.HttpResponseRedirect(durls.reverse('menu:program'))

	dish_set = set()
	for program2dish_form in program2dish_formset:
		try:
			dish_name = program2dish_form.cleaned_data.get('dish_name')
			if dish_name in dish_set:
				dmessages.error(request, "菜品%s输入了两次，请重新输入" % (dish_name))
				return dhettp.HttpResponseRedirect(durls.reverse('menu:program'))
			else:
				dish_set.add(dish_name)
			dish = Dish.objects.get(name = dish_name)
		except Dish.DoesNotExist:
			dmessages.error(request, "菜品%s不存在，请先添加菜品信息" % (dish_name))
			return dhttp.HttpResponseRedirect(durls.reverse('menu:program'))
		except Dish.MultipleObjectsReturned:
			dmessages.error(request, "记录中存在多个关于菜品%s的信息" % (dish_name))
			return dhttp.HttpResponseRedirect(durls.reverse('menu:program'))

	program_name = program_form.cleaned_data.get('program_name')
	date = program_form.cleaned_data.get('date')
	Program.objects.filter(name = program_name, date = date).delete()
	program = Program.objects.create(name = program_name, date = date)

	for program2dish_form in program2dish_formset:
		dish_name = program2dish_form.cleaned_data.get('dish_name')
		dish = Dish.objects.get(name = dish_name)
		count = program2dish_form.cleaned_data.get('count')
		Program2Dish.objects.create(program = program, dish = dish, count = count)

	dmessages.success(request, "成功添加项目!")
	return dhttp.HttpResponseRedirect(durls.reverse('menu:program'))


def program(request):
	if request.method == 'POST':
		return program_post(request)
	else:
		return program_get(request)