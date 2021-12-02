from datetime import date

from django.db import models

from common.models import Ingredient, Project


class ProjectPurchaseOrder(models.Model):
    project = models.ForeignKey(Project, models.CASCADE, verbose_name='项目')
    date = models.DateField(default=date.today, verbose_name='日期')

    class Meta:
        verbose_name = '项目采购清单'
        verbose_name_plural = '项目采购清单'

    def __str__(self):
        return '%s %s' % (str(self.project), str(self.date))


class ProjectPurchaseOrderItem(models.Model):
    order = models.ForeignKey(ProjectPurchaseOrder, models.CASCADE, related_name='items')
    ingredient = models.ForeignKey(Ingredient, models.SET_NULL, null=True, verbose_name='原材料')
    quantity = models.FloatField(verbose_name='数量')

    class Meta:
        verbose_name = '项目采购品'
        verbose_name_plural = '项目采购品'

    def __str__(self):
        return '%s %s' % (str(self.ingredient), self.quantity)


class PurchaseOrderSummary(models.Model):
    date = models.DateField(default=date.today, verbose_name='日期')

    class Meta:
        verbose_name = '采购清单汇总'
        verbose_name_plural = '采购清单汇总'

    def __str__(self):
        return str(self.date)


class PurchaseOrderSummaryItem(models.Model):
    summary = models.ForeignKey(PurchaseOrderSummary, models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE, null=True, verbose_name='原材料')
    quantity = models.FloatField(verbose_name='数量')

    class Meta:
        verbose_name = '采购品'
        verbose_name_plural = '采购品'

    def __str__(self):
        return '%s %s' % (str(self.ingredient), self.quantity)
