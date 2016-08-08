# -*- coding: utf-8 -*-

"""

    basic modules
    ~~~~~~~~~~~~~

    :Created: 2016-8-3
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from django.db import models

from utils.model_helper import GenericModelHelper


class BasicModule(models.Model,
                  GenericModelHelper):

    name = models.CharField(max_length=32, unique=True, blank=False)
    description = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "BasicModule"
