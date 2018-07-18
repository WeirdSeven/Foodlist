# -*- coding: utf-8 -*-  

import django.shortcuts as dshortcuts
import django.utils as dutils
import django.urls as durls
import django.http as dhttp
import django.forms as dforms
import django.contrib.messages as dmessages

import openpyxl

import datetime
import collections

from ..models import Program, Program2Dish, Dish, Dish2Ingredient, Ingredient
from . import excel

def report(request):
	program_list = list(Program.objects.all()).sort(key = lambda x : x.date, reverse = True)
	if not program_list:
		return dshortcuts.render(request, 'menu/reports.html')


	program_sublist = []

	print("p1")
	print(program_list)
	print("p2")

	last_sublist = -1
	for i in range(program_list):
		if i == 0 or program_list[i].date != program_list[i - 1].date:
			program_sublist.append([program_list[i]])
			last_sublist += 1
		else:
			program_sublist[last_sublist].append(program_list[i])

	return dshortcuts.render(request, 'menu/reports.html', context)

	#context = {
	#	'programs' : program_sublist
	#}

