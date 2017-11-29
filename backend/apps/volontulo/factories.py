# -*- coding: utf-8 -*-

"""
.. module:: factories
"""
import datetime
from django.contrib.auth import get_user_model
import factory
from factory.fuzzy import FuzzyChoice

from apps.volontulo.models import Organization, UserProfile, Offer


User = get_user_model()


class UserProfileFactory(factory.DjangoModelFactory):
    """Factory for user profile."""

    class Meta:  # pylint: disable=C0111
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):
    """Factory for User."""

    class Meta:  # pylint: disable=C0111
        model = User

    first_name = factory.Faker('first_name', locale='pl_PL')
    last_name = factory.Faker('last_name', locale='pl_PL')
    email = factory.Faker('email', locale='pl_PL')
    username = factory.LazyAttribute(lambda obj: obj.email)

    is_active = True
    password = 'password123'
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class OrganizationFactory(factory.DjangoModelFactory):
    """Factory for Organization."""

    def _organization_name():  # pylint: disable=E0211
        """Creates  a fake organization name.

        Fake name consist of predicate1 + subject + predicate2 + propername
        np. 'Wojewódzka Alternatywa Organizacyjna "Naprzód"'.
        """

        predicate1_dict = {
            'masculine': [
                'Krajowy', 'Wojewódzki', 'Powiatowy', 'Regionalny',
                'Wielkopolski', 'Osiedlowy', 'Stołeczny'],
            'feminine': [
                'Krajowa', 'Wojewódzka', 'Powiatowa', 'Regionalna',
                'Wielkopolska', 'Osiedlowa', 'Stołeczna'],
            'neutrum': [
                'Krajowe', 'Wojewódzkie', 'Powiatowe', 'Regionalne',
                'Wielkopolskie', 'Osiedlowe', 'Stołeczne']
            }
        noun_list = {
            'Fundacja': 'feminine',
            'Rada': 'feminine',
            'Urząd': 'masculine',
            'Zarząd': 'masculine',
            'Delegatura': 'feminine',
            'Poradnia': 'feminine',
            'Szpital': 'masculine',
            'Ogród': 'masculine',
            'Koło': 'neutrum',
            'Obwód': 'masculine'
            }
        predicate2_dict = {
            'masculine': [
                'Organizacyjny', 'Rejestrowy', 'Egzekutywny', 'Wspierający',
                'Transakcyjny', 'Związkowy', 'Zbiorczy'],
            'feminine': [
                'Organizacyjna', 'Rejestrowa', 'Egzekutywna', 'Wspierająca',
                'Transakcyjna', 'Związkowa', 'Zbiorcza'],
            'neutrum': [
                'Organizacyjne', 'Rejestrowe', 'Egzekutywne', 'Wspierające',
                'Transakcyjne', 'Związkowe', 'Zbiorcze']
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

        return '{0} {1} {2} {3}'.format(
            predicate1,
            subject,
            predicate2,
            propername
        )


    class Meta:  # pylint: disable=C0111
        model = Organization

    name = factory.fuzzy.FuzzyAttribute(_organization_name)
    address = factory.Faker('address', locale='pl_PL')
    description = factory.Faker('paragraph', locale='pl_PL')


class OfferFactory(factory.DjangoModelFactory):
    """Factory for Offer"""


    class Meta:  # pylint: disable=C0111
        model = Offer

    organization = factory.SubFactory(OrganizationFactory)

    @factory.post_generation
    def volunteers(self, create, extracted, **kwargs):  # pylint: disable=W0613
        '''Manage ManyToMany field'''

        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of Users were passed in, use them
            for user in extracted:
                self.user.add(user)

    description = factory.Faker('paragraph')
    requirements = factory.Faker('paragraph')
    time_commitment = factory.Faker('paragraph')
    benefits = factory.Faker('paragraph')
    location = factory.Faker('address', locale='pl_PL')
    title = factory.Faker('text', max_nb_chars=150)
    started_at = factory.fuzzy.FuzzyDate(datetime.date(2017, 11, 4))
    finished_at = factory.fuzzy.FuzzyDate(datetime.date(2017, 11, 4))
    time_period = factory.Faker('text', max_nb_chars=150)
    status_old = factory.fuzzy.FuzzyChoice(
        choices=('NEW', 'ACTIVE', 'SUSPENDED')
        )
    offer_status = factory.fuzzy.FuzzyChoice(
        choices=('unpublished', 'published', 'rejected')
        )
    recruitment_status = factory.fuzzy.FuzzyChoice(
        choices=('open', 'supplemental', 'closed')
        )
    action_status = factory.fuzzy.FuzzyChoice(
        choices=('future', 'ongoing', 'finished')
        )
    votes = factory.fuzzy.FuzzyChoice(choices=(0, 1))
    recruitment_start_date = factory.fuzzy.FuzzyDate(
        datetime.date(2017, 11, 4)
        )
    recruitment_end_date = factory.fuzzy.FuzzyDate(
        datetime.date(2017, 11, 4)
        )
    reserve_recruitment = factory.fuzzy.FuzzyChoice(choices=(0, 1))
    reserve_recruitment_start_date = factory.fuzzy.FuzzyDate(
        datetime.date(2017, 11, 4)
        )
    reserve_recruitment_end_date = factory.fuzzy.FuzzyDate(
        datetime.date(2017, 11, 4)
        )
    action_ongoing = factory.fuzzy.FuzzyChoice(choices=(0, 1))
    constant_coop = factory.fuzzy.FuzzyChoice(choices=(0, 1))
    action_start_date = factory.fuzzy.FuzzyDate(
        datetime.date(2008, 1, 1)
        )
    action_end_date = factory.fuzzy.FuzzyDate(
        datetime.date(2017, 11, 4)
        )
    volunteers_limit = factory.fuzzy.FuzzyInteger(0, 1000)
    weight = factory.fuzzy.FuzzyInteger(0, 1000)
