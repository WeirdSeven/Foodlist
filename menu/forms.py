# -*- coding: utf-8 -*-  

from django import forms
import datetime

class IngredientForm(forms.Form):
	name = forms.CharField(label = '名称')
	price = forms.FloatField(label = '价格（单位：元/斤）')
	ratio = forms.FloatField(label = '转化率')

class Dish2IngredientForm(forms.Form):
	ingredient_name = forms.CharField(widget=forms.TextInput(attrs={
									'placeholder': '原料名称',
									}))
	quantity = forms.FloatField()

class DishForm(forms.Form):
	dish_name = forms.CharField(widget=forms.TextInput(attrs={
								  'placeholder': '菜品名称',
								  }), label = '菜品名称')

class ProgramForm(forms.Form):
	program_name = forms.CharField(widget=forms.TextInput(attrs={
								  'placeholder': '项目名称',
								  }), label = '项目名称')
	date = forms.DateField(widget = forms.SelectDateWidget, initial = datetime.date.today, label = '日期')


class Program2DishForm(forms.Form):
	dish_name = forms.CharField(widget=forms.TextInput(attrs={
									'placeholder': '菜品名称',
									}))
	count = forms.IntegerField()

