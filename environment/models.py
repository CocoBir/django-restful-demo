# -*- coding: utf-8 -*-

"""

    environment management model design
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :Created: 2016-8-3
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from django.db import models

from basicmodule.models import BasicModule
from utils.model_helper import GenericModelHelper


class Environments(models.Model,
                   GenericModelHelper):
    """存储环境信息"""
    name = models.CharField(max_length=32, unique=True, blank=False)
    description = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "Environments"


class EnvModules(models.Model,
                 GenericModelHelper):
    """用于存储所有环境的模块信息"""
    name = models.CharField(max_length=32, unique=True, blank=False)
    moduleID = models.ForeignKey(
        BasicModule,
        db_column='moduleID',
        on_delete=models.CASCADE,
        related_name='envs'
    )
    envID = models.ForeignKey(
        Environments,
        db_column='envID',
        on_delete=models.CASCADE,
        related_name='entries' # use for select with environment to get all moduels
    )
    config = models.TextField(default="{}")

    class Meta:
        db_table = "EnvModules"
