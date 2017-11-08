# -*- coding: utf-8 -*-

"""
.. module:: factories
"""

import factory
from django.contrib.auth import get_user_model
from faker import Faker

from apps.volontulo.models import UserProfile

fake = Faker(locale='pl_PL')

User = get_user_model()


class UserProfileFactory(factory.DjangoModelFactory):
    """Factory for user profile."""

    class Meta:  # pylint: disable=C0111
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):
    """Factory for User."""

    class Meta:  # pylint: disable=C0111
        model = User

    first_name = fake.first_name()
    last_name = fake.last_name()
    username = factory.LazyAttribute(
        lambda obj: '{}.{}'.format(
            obj.first_name.lower(),
            obj.last_name.lower()
        )
    )
    email = factory.LazyAttribute(
        lambda obj: '{}@{}'.format(obj.username, fake.domain_name())
    )
    is_active = True
    password = 'password123'
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
