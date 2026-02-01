# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import uuid

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password, check_password


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True,
                          default=uuid.uuid7)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)  # Store hashed passwords, bcrypt
    internal_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, null=True, default=None)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, default=None)
    extras = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create_password(self, password: str):
        hash_ = make_password(password)
        self.password_hash = hash_
        return

    def check_password(self, password: str) -> bool:
        return check_password(password, self.password_hash)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_internal_user(sender: ty.Type[User], instance: User, created: bool, **kwargs):
    if not created:
        return

    if instance.internal_user:
        return

    internal_user = DjangoUser.objects.create_user(
        username=instance.username,
        email=instance.email,
        password=None  # No password for internal user
    )
    instance.internal_user = internal_user
    instance.save()
