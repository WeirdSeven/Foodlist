from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class Ingredient(models.Model):
	name = models.CharField(max_length = 200, verbose_name = '配料名称')
	ratio = models.FloatField(default = 1, verbose_name = '转化率')
	price = models.FloatField(verbose_name = '单价(元/斤)')

	class Meta:
		verbose_name = '配料'
		verbose_name_plural = '配料'

	def __str__(self):
		return self.name

class Dish(models.Model):
	name = models.CharField(max_length = 200, verbose_name = '菜品名称')
	ingredients = models.ManyToManyField(Ingredient, through = 'Dish2Ingredient')

	class Meta:
		verbose_name = '菜品'
		verbose_name_plural = '菜品'

	def __str__(self):
		return self.name

class Dish2Ingredient(models.Model):
	dish = models.ForeignKey(Dish, on_delete = models.CASCADE, verbose_name = '配料名称')
	ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, verbose_name = '菜品名称')
	quantity = models.FloatField(verbose_name = '重量')

	def __str__(self):
		return '%s %s %d斤' % (str(self.dish), str(self.ingredient), self.quantity)

class Program(models.Model):
	name = models.CharField(max_length = 200)
	date = models.DateField(default = datetime.date.today)
	dishes = models.ManyToManyField(Dish, through = 'Program2Dish')

	def __str__(self):
		return '%s %s' % (self.name, str(self.date))

class Program2Dish(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE)
	dish = models.ForeignKey(Dish, on_delete = models.CASCADE)
	count = models.IntegerField()

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.dish), self.count)
		