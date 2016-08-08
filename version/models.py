# -*- coding: utf-8 -*-

"""

    version management model design
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-3
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from django.db import models

from basicmodule.models import BasicModule
from utils.model_helper import GenericModelHelper


class Versions(models.Model,
               GenericModelHelper):
    """存储版本信息"""
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "Versions"


class VerModules(models.Model,
                 GenericModelHelper):
    """用于存储所有版本的模块信息"""
    name = models.CharField(max_length=32, unique=True)
    moduleID = models.ForeignKey(
        BasicModule,
        db_column='moduleID',
        on_delete=models.CASCADE,
        related_name='vers'
    )
    verID = models.ForeignKey(
        Versions,
        db_column='verID',
        on_delete=models.CASCADE,
        related_name='entries'
    )
    config = models.TextField(default="{}")

    class Meta:
        db_table = "VerModules"
