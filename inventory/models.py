from datetime import date

from django.contrib import admin
from django.db import models

from common.models import Ingredient, Project, RequestStatus


emoji_for_request_status = {
    RequestStatus.EDITING: '🕒',
    RequestStatus.SUBMITTED: '🈸',
    RequestStatus.APPROVED: '🟢',
    RequestStatus.REJECTED: '🔴',
    RequestStatus.REEDITING: '🈸',
    RequestStatus.RESUBMITTED: '🕒',
}


class InventoryInList(models.Model):
    project = models.ForeignKey(Project, models.CASCADE, verbose_name='项目')
    date = models.DateField(default=date.today, verbose_name='日期')
    comments = models.TextField(verbose_name='评论')
    status = models.CharField(
        max_length=3,
        choices=RequestStatus.choices,
        default=RequestStatus.EDITING,
        verbose_name='状态'
    )

    class Meta:
        verbose_name = '入库单'
        verbose_name_plural = '入库单'
        permissions = [("edit_comments", "Can edit comments")]

    @admin.display(description='状态')
    def emoji_and_status(self):
        status = RequestStatus(self.status)
        return f'{emoji_for_request_status[status]} {status.label}'

    def __str__(self):
        return f'{self.project} {self.date}'


class InventoryInListItem(models.Model):
    in_list = models.ForeignKey(InventoryInList, models.CASCADE, related_name='in_items')
    ingredient = models.ForeignKey(Ingredient, models.SET_NULL, null=True, verbose_name='原材料')
    quantity = models.FloatField(verbose_name='数量')

    def __str__(self):
        return f'{self.ingredient} {self.quantity}'


class InventoryOutList(models.Model):
    project = models.ForeignKey(Project, models.CASCADE, verbose_name='项目')
    date = models.DateField(default=date.today, verbose_name='日期')
    comments = models.TextField(verbose_name='评论')
    status = models.CharField(
        max_length=3,
        choices=RequestStatus.choices,
        default=RequestStatus.EDITING,
        verbose_name='状态'
    )

    class Meta:
        verbose_name = '出库单'
        verbose_name_plural = '出库单'


class InventoryOutListItem(models.Model):
    out_list = models.ForeignKey(InventoryInList, models.CASCADE, related_name='out_items')
    ingredient = models.ForeignKey(Ingredient, models.SET_NULL, null=True, verbose_name='原材料')
    quantity = models.FloatField(verbose_name='数量')

