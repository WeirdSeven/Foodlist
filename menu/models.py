from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class Ingredient(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '配料名称')
	ratio = models.FloatField(default = 1, verbose_name = '转化率')
	price = models.FloatField(verbose_name = '单价(元/斤)')

	class Meta:
		verbose_name = '配料'
		verbose_name_plural = '配料'

	def __str__(self):
		return self.name

class Dish(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '菜品名称')
	ingredients = models.ManyToManyField(Ingredient, through = 'Dish2Ingredient')

	class Meta:
		verbose_name = '菜品'
		verbose_name_plural = '菜品'

	def __str__(self):
		return self.name

class Dish2Ingredient(models.Model):
	dish = models.ForeignKey(Dish, on_delete = models.CASCADE, verbose_name = '菜品名称')
	ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, verbose_name = '配料名称')
	quantity = models.FloatField(verbose_name = '重量')

	class Meta:
		verbose_name = '菜品的配料'
		verbose_name_plural = '菜品的配料'

	def __str__(self):
		return '%s %s %d斤' % (str(self.dish), str(self.ingredient), self.quantity)

class Program(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '项目名称')
	date = models.DateField(default = datetime.date.today, verbose_name = '日期')
	dishes = models.ManyToManyField(Dish, through = 'Program2Dish')

	class Meta:
		verbose_name = '项目'
		verbose_name_plural = '项目'

	def __str__(self):
		return '%s %s' % (self.name, str(self.date))

class Program2Dish(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE, verbose_name = '项目名称')
	dish = models.ForeignKey(Dish, on_delete = models.CASCADE, verbose_name = '菜品名称')
	count = models.IntegerField(verbose_name = '份数')

	class Meta:
		verbose_name = '项目的菜品'
		verbose_name_plural = '项目的菜品'

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.dish), self.count)
