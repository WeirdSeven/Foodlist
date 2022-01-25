from datetime import date

from django.contrib import admin
from django.db import models

from common.models import Ingredient, Project


class ApprovalStatus(models.TextChoices):
    EDITING = 'EDT', '编辑中'
    SUBMITTED = 'SBM', '已提交'
    APPROVED = 'APR', '️️通过'
    REJECTED = 'REJ', '未通过'
    REEDITING = 'RED', '重新编辑中'
    RESUBMITTED = 'RSB', '已重新提交'


emoji_for_approval_status = {
    ApprovalStatus.EDITING: '🕒',
    ApprovalStatus.SUBMITTED: '🈸',
    ApprovalStatus.APPROVED: '🟢',
    ApprovalStatus.REJECTED: '🔴',
    ApprovalStatus.REEDITING: '🈸',
    ApprovalStatus.RESUBMITTED: '🕒',
}


class InventoryInList(models.Model):
    project = models.ForeignKey(Project, models.CASCADE, verbose_name='项目')
    date = models.DateField(default=date.today, verbose_name='日期')
    comments = models.TextField(verbose_name='评论')
    status = models.CharField(
        max_length=3,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.EDITING,
        verbose_name='状态'
    )

    class Meta:
        verbose_name = '入库单'
        verbose_name_plural = '入库单'
        permissions = [("edit_comments", "Can edit comments")]

    @admin.display(description='状态')
    def emoji_and_status(self):
        status = ApprovalStatus(self.status)
        return f'{emoji_for_approval_status[status]} {status.label}'

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
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.EDITING,
        verbose_name='状态'
    )

    class Meta:
        verbose_name = '出库单'
        verbose_name_plural = '出库单'


class InventoryOutListItem(models.Model):
    out_list = models.ForeignKey(InventoryInList, models.CASCADE, related_name='out_items')
    ingredient = models.ForeignKey(Ingredient, models.SET_NULL, null=True, verbose_name='原材料')
    quantity = models.FloatField(verbose_name='数量')

