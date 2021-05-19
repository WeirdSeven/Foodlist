# -*- coding: utf-8 -*-  

import django.shortcuts as dshortcuts
import django.utils as dutils
import django.urls as durls
import django.http as dhttp
import django.forms as dforms
import django.contrib.messages as dmessages
from django.utils.encoding import smart_str

import openpyxl

import datetime
import collections
import os

from ..models import SuperProgram, Program, Program2Dish, Dish, Dish2Ingredient, Ingredient
from . import reportutils


def report_list(request):
	program_list = list(Program.objects.all().order_by('-date'))
	if not program_list:
		context = {
			'today': datetime.date.today(),
			'program_sublists': [],
		}
		return dshortcuts.render(request, 'menu/reports.html', context)

	class ProgramSublist:
		def __init__(self, date):
			self.date = date
			self.programs = []
			self.super_programs = {}

		def __repr__(self):
			return "ProgramSublist(%r, %r)" % (self.date, self.programs)

	program_sublists = []
	for i in range(len(program_list)):
		if i == 0 or program_list[i].date != program_list[i - 1].date:
			new_program_sublist = ProgramSublist(program_list[i].date)
			new_program_sublist.programs.append(program_list[i])
			new_program_sublist.super_programs[program_list[i].superprogram] = None
			program_sublists.append(new_program_sublist)
		else:
			program_sublists[-1].programs.append(program_list[i])
			program_sublists[-1].super_programs[program_list[i].superprogram] = None

	context = {
		'today' : datetime.date.today(),
		'program_sublists' : program_sublists,
	}

	return dshortcuts.render(request, 'menu/reports.html', context)

def report_post(request, year, month, day):
	reports_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'reports')
	if not os.path.exists(reports_directory):
		os.makedirs(reports_directory)

	# Genetes spreadsheets for programs
	programs_to_update = Program.objects.filter(date = datetime.date(year, month, day))
	for program in programs_to_update:
		title = reportutils.report_title(year, month, day, program.name, False)
		reportutils.program_report(program, title).save('reports/%s.xlsx' % title)

	super_programs = collections.defaultdict(list)
	for program in programs_to_update:
		super_programs[program.superprogram.name].append(program)
	for super_program_name, programs in super_programs.items():
		title = reportutils.report_title(year, month, day, super_program_name, True)
		reportutils.company_report(programs, title).save('reports/%s.xlsx' % title)

	# Generates spreadsheets for company
	title = reportutils.report_title(year, month, day)
	reportutils.company_report(programs_to_update, title).save('reports/%s.xlsx' % title)

	dmessages.success(request, "成功更新了所有今日报告")
	return dhttp.HttpResponseRedirect(durls.reverse('menu:reports'))

def report_get(request, year, month, day, program=None, is_super_program=False):
	reports_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'reports')
	filename = '%s.xlsx' % reportutils.report_title(year, month, day, program, is_super_program)
	filepath = os.path.join(reports_directory, filename)
	if not os.path.exists(filepath):
		dmessages.error(request, "该文件不存在")
		return dhttp.HttpResponseRedirect(durls.reverse('menu:reports'))
	else:
		with open(filepath, 'rb') as excel:
			data = excel.read()

		response = dhttp.HttpResponse(content = data, content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] =  reportutils.rfc5987_content_disposition(filename)
		return response

def report(request, year, month, day, program=None, is_super_program=False):
	if request.method == 'POST':
		return report_post(request, year, month, day)
	else:
		return report_get(request, year, month, day, program, is_super_program)



