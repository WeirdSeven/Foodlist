from __future__ import unicode_literals
from datetime import date

from django.db import models

from common.models import Project, SDish2Standard


class Meal(models.TextChoices):
    BREAKFAST = 'B', '早餐'
    LUNCH = 'L', '午餐'
    DINNER = 'D', '晚餐'
    MIDNIGHT = 'M', '夜餐'


class Course(models.TextChoices):
    PRIMARY_MEAT = 'PM', '主荤'
    SECONDARY_MEAT = 'SM', '次荤'
    VEGETABLE = 'VG', '素菜'
    SPECIAL = 'SP', '特色'
    FRUIT = 'FR', '水果'
    GRAIN = 'GR', '杂粮'
    SOUP = 'SU', '汤粥'
    STAPLE = 'ST', '主食'
    SIDE = 'SD', '副食'
    COLD = 'CD', '凉菜'
    PICKLE = 'PK', '咸菜'


# Central Kitchen Projects

class CKProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='中央厨房项目名称')
    date = models.DateField(default=date.today, verbose_name='日期')

    sdish2standards = models.ManyToManyField(SDish2Standard, through='CKProject2SDish2Standard')

    class Meta:
        verbose_name = '中央厨房菜单'
        verbose_name_plural = '中央厨房菜单'

    def __str__(self):
        return f'{self.project} {self.date}'


class CKProject2SDish2Standard(models.Model):
    project = models.ForeignKey(
        CKProject,
        on_delete=models.CASCADE,
        verbose_name='中央厨房项目名称'
    )
    sdish2standard = models.ForeignKey(
        SDish2Standard,
        on_delete=models.CASCADE,
        verbose_name='菜品名称'
    )

    meal = models.CharField(
        max_length=1,
        choices=Meal.choices,
        default=Meal.LUNCH,
        verbose_name='用餐时间'
    )
    course = models.CharField(
        max_length=2,
        choices=Course.choices,
        default=Course.PRIMARY_MEAT,
        verbose_name='菜品分类'
    )

    class Meta:
        verbose_name = '项目菜品'
        verbose_name_plural = '项目菜品'

    def __str__(self):
        return f'{self.project} {self.sdish2standard}'


class CKProjectLocation(models.Model):
    name = models.CharField(max_length=200, verbose_name='中央厨房送餐点名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')

    class Meta:
        verbose_name = '中央厨房送餐点'
        verbose_name_plural = '中央厨房送餐点'

    def __str__(self):
        return self.name


class CKProject2SDish2StandardCount(models.Model):
    project2dish2standard = models.ForeignKey(
        CKProject2SDish2Standard,
        on_delete=models.CASCADE,
        related_name='locations_counts')
    location = models.ForeignKey(
        CKProjectLocation,
        on_delete=models.CASCADE,
        verbose_name='送餐点')
    count = models.IntegerField(verbose_name='份数')

    class Meta:
        verbose_name = '送餐点及份数'
        verbose_name_plural = '送餐点及份数'

    def __str__(self):
        return f'{self.location} {self.count}份'
