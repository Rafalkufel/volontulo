# -*- coding: utf-8 -*-

"""
.. module:: factories
"""

from django.contrib.auth import get_user_model
import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from apps.volontulo.models import Organization, UserProfile


User = get_user_model()


def organization_name():
    """Creates organization name consist of
    predicate 1 + subject + predicate2 + propername
    np. Wojewódzka Alternatywa Organizacyjna "Naprzód" """
    
    predicate1_dict = {
        'meski': [
            'Krajowy', 'Wojewódzki', 'Powiatowy', 'Regionalny',
            'Wielkopolski', 'Osiedlowy', 'Stołeczny'],
        'zenski': [
            'Krajowa', 'Wojewódzka', 'Powiatowa', 'Regionalna',
            'Wielkopolska', 'Osiedlowa', 'Stołeczna'],
        'nijaki': [
            'Krajowe', 'Wojewódzkie', 'Powiatowe', 'Regionalne',
            'Wielkopolskie', 'Osiedlowe', 'Stołeczne']
        }
    noun_list = {
        'Fundacja': 'zenski',
        'Rada': 'zenski',
        'Urząd': 'meski',
        'Zarząd': 'meski',
        'Delegatura': 'zenski',
        'Poradnia': 'zenski',
        'Szpital': 'meski',
        'Ogród': 'meski',
        'Koło': '3',
        'Obwód': 'meski'
        }
    predicate2_dict = {
        'meski': [
            'Organizacyjny', 'Rejestrowy', 'Egzekutywny', 'Wspierający',
            'Tranakcyjny', 'Związkowy', 'Zbiorczy'],
        'zenski': [
            'Organizacyjna', 'Rejestrowa', 'Egzekutywna', 'Wspierająca',
            'Tranakcyjna', 'Związkowa', 'Zbiorcza'],
        'nijaki': [
            'Organizacyjne', 'Rejestrowe', 'Egzekutywne', 'Wspierające',
            'Tranakcyjne', 'Związkowe', 'Zbiorcze']
        }

    propername_list = [
        '"Wspiera się"', '"Totuus"', '"Zawsze Razem"', '"W Kupie Siła"',
        '"Al Capone"', '"UKF"', '"Smak Miesiąca"'
        ]

    # FuzzyChoice object

    subject = (FuzzyChoice(noun_list.keys())).fuzz()
    predicate1 = (FuzzyChoice(predicate1_dict[noun_list[subject]])).fuzz()
    predicate2 = (FuzzyChoice(predicate2_dict[noun_list[subject]])).fuzz()
    propername = (FuzzyChoice(propername_list)).fuzz()

    return '{0} {1} {2} {3}'.format(predicate1, subject, predicate2, propername)


class UserProfileFactory(factory.DjangoModelFactory):
    """Factory for user profile."""

    class Meta:  # pylint: disable=C0111
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):
    """Factory for User."""

    class Meta:  # pylint: disable=C0111
        model = User

    # address = factory.Faker('address', locale='pl_PL')

    first_name = factory.Faker('first_name', locale='pl_PL')
    last_name = factory.Faker('last_name', locale='pl_PL')
    email = factory.Faker('email', locale='pl_PL')
    username = factory.LazyAttribute(lambda obj: obj.email)

    is_active = True
    password = 'password123'
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     manager = cls._get_manager(model_class)
    #     return manager.create_user(*args, **kwargs)


class OrganizationFactory(factory.DjangoModelFactory):
    """Factory for Organization"""

    class Meta:
        model = Organization

    name = factory.fuzzy.FuzzyAttribute(organization_name)
    address = factory.Faker('address', locale='pl_PL')
    description = factory.Faker('paragraph', locale='pl_PL')

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     manager = cls._get_manager(model_class)
    #     return manager.create_organization(*args, **kwargs)
