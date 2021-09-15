from __future__ import unicode_literals

from django.db import models
import datetime

class Ingredient(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '配料名称')
	ratio = models.FloatField(default = 1, verbose_name = '转化率')
	price = models.FloatField(verbose_name = '单价(元/斤)')

	class Meta:
		verbose_name = '配菜'
		verbose_name_plural = '配菜'

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
	ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, verbose_name = '配菜名称')
	quantity = models.FloatField(verbose_name = '重量')

	class Meta:
		verbose_name = '菜品的配菜'
		verbose_name_plural = '菜品的配菜'

	def __str__(self):
		return '%s %s %d' % (str(self.dish), str(self.ingredient), self.quantity)

class CongeeSoup(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '汤粥名称')
	ingredient = models.ManyToManyField(Ingredient, through = 'CongeeSoup2Ingredient')

	class Meta:
		verbose_name = '汤粥'
		verbose_name_plural = '汤粥'

	def __str__(self):
		return self.name

class CongeeSoup2Ingredient(models.Model):
	congeesoup = models.ForeignKey(CongeeSoup, on_delete = models.CASCADE, verbose_name = '汤粥名称')
	ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE, verbose_name = '配菜名称')
	quantity = models.FloatField(verbose_name = '重量')

	class Meta:
		verbose_name = '汤粥的配菜'
		verbose_name_plural = '汤粥的配菜'

	def __str__(self):
		return '%s %s %d' % (str(self.congeesoup), str(self.ingredient), self.quantity)

class Staple(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '主食名称')
	price = models.FloatField(verbose_name = '单价')

	class Meta:
		verbose_name = '主食'
		verbose_name_plural = '主食'

	def __str__(self):
		return self.name

class Oil(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '油名称')
	price = models.FloatField(verbose_name = '单价')

	class Meta:
		verbose_name = '油'
		verbose_name_plural = '油'

	def __str__(self):
		return self.name

class Condiment(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '调料名称')
	price = models.FloatField(verbose_name = '单价')

	class Meta:
		verbose_name = '调料'
		verbose_name_plural = '调料'

	def __str__(self):
		return self.name

class Disposable(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '一次性用品名称')
	price = models.FloatField(verbose_name = '单价')

	class Meta:
		verbose_name = '一次性用品'
		verbose_name_plural = '一次性用品'

	def __str__(self):
		return self.name


class SuperProgram(models.Model):
	name = models.CharField(max_length = 200, unique = True, verbose_name = '大项目名称')

	class Meta:
		verbose_name = '大项目'
		verbose_name_plural = '大项目'

	def __str__(self):
		return self.name

class Program(models.Model):
	name = models.CharField(max_length = 200, verbose_name = '项目名称')
	superprogram = models.ForeignKey(SuperProgram, null = True, on_delete = models.SET_NULL, verbose_name = '大项目名称')
	date = models.DateField(default = datetime.date.today, verbose_name = '日期')

	dishes = models.ManyToManyField(Dish, through = 'Program2Dish')
	congeesoups = models.ManyToManyField(CongeeSoup, through = 'Program2CongeeSoup')
	staples = models.ManyToManyField(Staple, through = 'Program2Staple')
	condiments_bool = models.BooleanField(verbose_name = '点击使用此调料价格而非下面表格的调料明细')
	condiments_price = models.FloatField(verbose_name = '项目的调料价格')
	condiments = models.ManyToManyField(Condiment, through = 'Program2Condiment')
	oil = models.ManyToManyField(Oil, through = 'Program2Oil')
	disposables = models.ManyToManyField(Disposable, through = 'Program2Disposable')

	class Meta:
		verbose_name = '项目'
		verbose_name_plural = '项目'
		constraints = [models.UniqueConstraint(fields=['name', 'date'], name='program-name-date-unique')]

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

class Program2CongeeSoup(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE, verbose_name = '项目名称')
	congeesoup = models.ForeignKey(CongeeSoup, on_delete = models.CASCADE, verbose_name = '汤粥名称')
	count = models.IntegerField(verbose_name = '份数')

	class Meta:
		verbose_name = '项目的汤粥'
		verbose_name_plural = '项目的汤粥'

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.congeesoup), self.count)

class Program2Staple(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE, verbose_name = '项目名称')
	staple = models.ForeignKey(Staple, on_delete = models.CASCADE, verbose_name = '主食名称')
	count = models.IntegerField(verbose_name = '用量')

	class Meta:
		verbose_name = '项目的主食'
		verbose_name_plural = '项目的主食'

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.staple), self.count)

class Program2Oil(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE, verbose_name = '项目名称')
	oil = models.ForeignKey(Oil, on_delete = models.CASCADE, verbose_name = '油名称')
	count = models.IntegerField(verbose_name = '用量')

	class Meta:
		verbose_name = '项目的油'
		verbose_name_plural = '项目的油'

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.oil), self.count)

class Program2Condiment(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE, verbose_name = '项目名称')
	condiment = models.ForeignKey(Condiment, on_delete = models.CASCADE, verbose_name = '调料名称')
	count = models.IntegerField(verbose_name = '用量')

	class Meta:
		verbose_name = '项目的调料'
		verbose_name_plural = '项目的调料'

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.condiment), self.count)

class Program2Disposable(models.Model):
	program = models.ForeignKey(Program, on_delete = models.CASCADE, verbose_name = '项目名称')
	disposable = models.ForeignKey(Disposable, on_delete = models.CASCADE, verbose_name = '一次性用品名称')
	count = models.IntegerField(verbose_name = '用量')

	class Meta:
		verbose_name = '项目的一次性用品'
		verbose_name_plural = '项目的一次性用品'

	def __str__(self):
		return '%s %s %d' % (str(self.program), str(self.disposable), self.count)


# Standardized dishes
class SDish(models.Model):
	name = models.CharField(max_length=200, unique=True, verbose_name='菜品名称')

	class Meta:
		verbose_name = '菜品'
		verbose_name_plural = '菜品'

	def __str__(self):
		return self.name


class SDish2Standard(models.Model):
	dish = models.ForeignKey(SDish, on_delete=models.CASCADE, verbose_name='菜品名称')
	standard = models.CharField(max_length=200, verbose_name='标准名称')

	class Meta:
		verbose_name = '菜品标准'
		verbose_name_plural = '菜品标准'

	def __str__(self):
		return '%s %s' % (str(self.dish), str(self.standard))

class SDish2StandardIngredient(models.Model):
	sdish2standard = models.ForeignKey(SDish2Standard, on_delete=models.CASCADE)

	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='配菜名称')
	quantity = models.FloatField(verbose_name='重量')

	class Meta:
		verbose_name = '此标准的配菜'
		verbose_name_plural = '此标准的配菜'

	def __str__(self):
		return ''

# Central Kitchen Projects
class Meal(models.TextChoices):
	BREAKFAST = 'B', '早餐'
	LUNCH = 'L', '午餐'
	DINNER = 'D', '晚餐'
	MIDNIGHT = 'M', '夜餐'

class Course(models.TextChoices):
	PRIMARY_MEAT = 'PM', '主荤'
	SECONDARY_MEAT = 'SM', '次荤'
	VEGETABLES = 'VG', '素菜'
	SPECIALS = 'SP', '特色'

class CKProject(models.Model):
	name = models.CharField(max_length=200, verbose_name='中央厨房项目名称')
	date = models.DateField(default=datetime.date.today, verbose_name='日期')

	sdishe2standards = models.ManyToManyField(SDish2Standard, through='CKProject2SDish2Standard')

	class Meta:
		verbose_name = '中央厨房项目'
		verbose_name_plural = '中央厨房项目'

	def __str__(self):
		return '%s %s' % (self.name, str(self.date))


class CKProject2SDish2Standard(models.Model):
	project = models.ForeignKey(CKProject, on_delete=models.CASCADE, verbose_name='中央厨房项目名称')
	sdish2standard = models.ForeignKey(SDish2Standard, on_delete=models.CASCADE, verbose_name='菜品名称')

	meal = models.CharField(max_length=1, choices=Meal.choices, default=Meal.LUNCH, verbose_name='用餐时间')
	course = models.CharField(max_length=2, choices=Course.choices, default=Course.PRIMARY_MEAT, verbose_name='菜品分类')

	class Meta:
		verbose_name = '项目菜品'
		verbose_name_plural = '项目菜品'

	def __str__(self):
		return ''

class CKProjectLocation(models.Model):
	name = models.CharField(max_length=200, verbose_name='中央厨房餐点名称')

	class Meta:
		verbose_name = '中央厨房餐点'
		verbose_name_plural = '中央厨房餐点'

	def __str__(self):
		return self.name

class CKProject2SDish2StandardCount(models.Model):
	project2dish2standard = models.ForeignKey(CKProject2SDish2Standard, on_delete=models.CASCADE)

	location = models.ForeignKey(CKProjectLocation, on_delete=models.CASCADE, verbose_name='送餐点')
	count = models.IntegerField(verbose_name='份数')

	class Meta:
		verbose_name = '送餐点及份数'
		verbose_name_plural = '送餐点及份数'

	def __str__(self):
		return ''
