from django.contrib import admin
from django.db import models


# Ingredient

class IngredientCategory(models.TextChoices):
    VEGETABLE = 'VG', '蔬果'
    MEAT = 'MT', '肉类'
    TOFU = 'TF', '豆制品'
    CONDIMENT = 'CND', '调料'
    DRY = 'DRY', '干货'
    RICE_NOODLE_OIL = 'RNO', '米面油'
    DISPOSABLE = 'DSP', '低值易耗'


class IngredientUnit(models.TextChoices):
    JIN = 'JN', '斤'
    KILOGRAM = 'KG', '公斤'
    BOTTLE = 'BT', '瓶'
    BUCKET = 'BK', '桶'
    BOX = 'BX', '箱'
    SACK = 'SK', '袋'
    BAG = 'BG', '包'


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='原材料名称')
    category = models.CharField(
        max_length=3,
        choices=IngredientCategory.choices,
        default=IngredientCategory.VEGETABLE,
        verbose_name='分类'
    )
    specification = models.CharField(max_length=200, blank=True, verbose_name='规格')
    ratio = models.FloatField(default=1, verbose_name='转化率')
    price = models.FloatField(verbose_name='单价')
    unit = models.CharField(
        max_length=2,
        choices=IngredientUnit.choices,
        default=IngredientUnit.JIN,
        verbose_name='单位'
    )

    class Meta:
        verbose_name = '原材料'
        verbose_name_plural = '原材料'

    @property
    @admin.display(description='品名')
    def name_and_spec(self):

        def specification_paretheses():
            if self.specification:
                return f'（{self.specification}）'
            else:
                return ' '

        return f'{self.name}{specification_paretheses()}'

    @property
    @admin.display(description='单价')
    def price_per_unit(self):

        def format_without_zero(f):
            if f.is_integer():
                return int(f)
            else:
                return f

        return f'{format_without_zero(self.price)}元/{IngredientUnit(self.unit).label}'

    def __str__(self):
        return f'{self.name_and_spec}{self.price_per_unit}'


# Project
class ProjectType(models.TextChoices):
    CENTRAL_KITCHEN = 'CK', '中央厨房'
    DINING_HALL = 'DH', '食堂'


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='项目名称')
    type = models.CharField(
        max_length=2,
        choices=ProjectType.choices,
        default=ProjectType.DINING_HALL,
        verbose_name='项目类型'
    )

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.name


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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')

    class Meta:
        verbose_name = '菜品标准'
        verbose_name_plural = '菜品标准'

    def __str__(self):
        # Use the Chinese parentheses (2 characters)
        return '%s（%s）' % (str(self.dish), str(self.standard))


class SDish2StandardIngredient(models.Model):
    sdish2standard = models.ForeignKey(
        SDish2Standard,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='原材料名称')
    quantity = models.FloatField(verbose_name='重量')

    class Meta:
        verbose_name = '此标准的原材料'
        verbose_name_plural = '此标准的原材料'

    def __str__(self):
        return f'{self.sdish2standard} {self.ingredient}'
