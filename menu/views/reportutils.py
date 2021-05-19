# -*- coding: utf-8 -*-  

import django.utils.http as duhttp

import openpyxl

import collections
import unicodedata

from ..models import Program, Program2Dish, Dish, Dish2Ingredient, Ingredient
from . import excel

def report_title(year, month, day, name=None, is_super_program=False):
	if name:
		if is_super_program:
			return '%d年%d月%d日%s大项目' % (year, month, day, name)
		else:
			return '%d年%d月%d日%s项目' % (year, month, day, name)
	else:
		return '%d年%d月%d日公司' % (year, month, day)

def rfc5987_content_disposition(file_name):
	ascii_name = unicodedata.normalize('NFKD', file_name).encode('ascii','ignore').decode()
	header = 'attachment; filename="{}"'.format(ascii_name)
	if ascii_name != file_name:
		quoted_name = duhttp.urlquote(file_name)
		header += '; filename*=UTF-8\'\'{}'.format(quoted_name)

	return header


def get_dish_ingredients(dish):
	dish2ingredient_entries = Dish2Ingredient.objects.filter(dish = dish)
	return [(entry.ingredient.name, entry.quantity) for entry in dish2ingredient_entries]


def program_report(program, title):
	program2dish_entries = Program2Dish.objects.filter(program = program)

	program_dishes = []
	program_ingredient_map = collections.OrderedDict()
	for i, entry in enumerate(program2dish_entries, start = 1):
		dish_ingredients = get_dish_ingredients(entry.dish)
		dish_ingredients = [(ingredient[0], ingredient[1] * entry.count) for ingredient in dish_ingredients]
		program_dishes.append((i, entry.dish.name, entry.count, dish_ingredients))
		for ingredient in dish_ingredients:
			program_ingredient_map[ingredient[0]] = program_ingredient_map.get(ingredient[0], 0) + ingredient[1]

	program_ingredients = []
	for i, (ingredient_name, ingredient_quantity) in enumerate(list(program_ingredient_map.items()), start = 1):
		ingredient = Ingredient.objects.get(name = ingredient_name)
		raw_quantity = ingredient_quantity / ingredient.ratio
		cost = raw_quantity * ingredient.price
		program_ingredients.append((i, ingredient_name, raw_quantity, cost))

	wb = excel.program_ingredient_report(title, program_dishes, program_ingredients)
	return wb

	'''
	response = dhttp.HttpResponse(content = openpyxl.writer.excel.save_virtual_workbook(wb), 
		content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	filename = '%d年%d %d %s.xlsx' % (year, month, day, name)
	response['Content-Disposition'] = 'attachment; filename=%s' % dutils.encoding.force_text(filename)
	return response
	'''

def company_report(programs, title):
	program_names = [program.name for program in programs]

	program2dish_entries = []
	for program in programs:
		program2dish_entries.extend(list(Program2Dish.objects.filter(program = program)))

	# Get all unique dishes
	program_dishes = collections.OrderedDict()
	for entry in program2dish_entries:
		program_dishes[entry.dish] = None
	program_dishes = list(program_dishes.keys())

	# Get dish info of the company
	company_dishes = []
	company_ingredient_map = collections.OrderedDict()
	for i, dish in enumerate(program_dishes, start = 1):
		total_count = 0
		count_breakdown = []
		for program in programs:
			try:
				count = Program2Dish.objects.get(program = program, dish = dish).count
			except Program2Dish.DoesNotExist:
				count = 0
			count_breakdown.append(count)
			total_count += count

		dish_ingredients = get_dish_ingredients(dish)
		dish_ingredients = [(name, quantity * total_count) for name, quantity in dish_ingredients]

		company_dishes.append((i, dish.name, count_breakdown, dish_ingredients))
		for ingredient in dish_ingredients:
			company_ingredient_map[ingredient[0]] = company_ingredient_map.get(ingredient[0], 0) + ingredient[1]

	company_ingredients = []
	for i, (ingredient_name, ingredient_quantity) in enumerate(list(company_ingredient_map.items()), start = 1):
		ingredient = Ingredient.objects.get(name = ingredient_name)
		raw_quantity = ingredient_quantity / ingredient.ratio
		cost = raw_quantity * ingredient.price
		company_ingredients.append((i, ingredient_name, raw_quantity, cost))

	wb = excel.company_ingredient_report(title, program_names, company_dishes, company_ingredients)
	return wb

	'''
	response = dhttp.HttpResponse(content = openpyxl.writer.excel.save_virtual_workbook(wb), 
		content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename=%d年%d月%d日公司总配料单.xlsx' % (year, month, day)
	return response
	'''