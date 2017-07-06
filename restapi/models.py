# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

#
# class CustomUser(AbstractUser):
#     gender = models.CharField(max_length=10,null=True)
#     city = models.CharField(max_length=25,null=True)
#     userType = models.CharField(max_length=25,null=True) #Student,Professional,Admin
#     FavoriteLanguage = models.CharField(max_length=25,null=True)
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,null=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    userType = models.CharField(max_length=25, null=True)   #student professional
    FavoriteLanguage = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.user.username
