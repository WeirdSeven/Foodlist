from datetime import date

from django.contrib import admin
from django.db import models


# Ingredient

class IngredientCategory(models.TextChoices):
    VEGETABLE = 'VG', '蔬果'
    MEAT = 'MT', '肉类'
    SIDE = 'SD', '副食'
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
    SINGLE = 'SN', '个'
    PAIR = 'PR', '副'


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
    def latest_price(self):
        prices = self.prices.order_by('-effective_date')
        if prices:
            return prices[0].price

    def effective_price(self, request_date):
        prices = self.prices.order_by('-effective_date')
        for price in prices:
            if request_date > price.effective_date:
                return price.price

    def price_per_unit(self, price):

        def format_without_zero(f):
            if f.is_integer():
                return int(f)
            else:
                return f

        if price:
            return f'{format_without_zero(price)}元/{IngredientUnit(self.unit).label}'

    @property
    @admin.display(description='单价')
    def latest_price_per_unit(self):
        return self.price_per_unit(self.latest_price)

    def effective_price_per_unit(self, request_date):
        return self.price_per_unit(self.effective_price(request_date))

    def __str__(self):
        return f'{self.name_and_spec}{self.latest_price_per_unit}'


class IngredientPrice(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        models.CASCADE,
        verbose_name='原材料',
        related_name='prices'
    )
    price = models.FloatField(verbose_name='单价')
    effective_date = models.DateField(default=date.today, verbose_name='生效日期')

    class Meta:
        verbose_name = '原材料价格'
        verbose_name_plural = '原材料价格'

    def __str__(self):
        return f'{self.ingredient} {self.price} {self.effective_date}'


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


# Requests

class RequestStatus(models.TextChoices):
    EDITING = 'EDT', '编辑中'
    SUBMITTED = 'SBM', '已提交'
    APPROVED = 'APR', '️️通过'
    REJECTED = 'REJ', '未通过'
    REEDITING = 'RED', '重新编辑中'
    RESUBMITTED = 'RSB', '已重新提交'
