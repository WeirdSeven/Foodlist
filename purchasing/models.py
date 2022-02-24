from datetime import date

from django.contrib import admin
from django.db import models

from common.models import Ingredient, Project, RequestStatus


class ProjectSettings(models.Model):
    project = models.OneToOneField(
        Project,
        models.CASCADE,
        verbose_name='项目',
        related_name='purchasing_settings'
    )
    daily_purchasing_budget = models.FloatField(verbose_name='每日采购成本上限')

    class Meta:
        verbose_name = '项目采购设置'
        verbose_name_plural = '项目采购设置'

    def __str__(self):
        return f'{self.project}采购设置'


emoji_for_request_status = {
    RequestStatus.EDITING: '🕒',
    RequestStatus.SUBMITTED: '🟢'
}


class ProjectPurchaseOrder(models.Model):
    project = models.ForeignKey(Project, models.CASCADE, verbose_name='项目')
    date = models.DateField(default=date.today, verbose_name='日期')
    status = models.CharField(
        max_length=3,
        choices=RequestStatus.choices,
        default=RequestStatus.EDITING,
        verbose_name='状态'
    )

    class Meta:
        verbose_name = '项目采购清单'
        verbose_name_plural = '项目采购清单'

    @admin.display(description='状态')
    def emoji_and_status(self):
        status = RequestStatus(self.status)
        return f'{emoji_for_request_status[status]} {status.label}'

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
