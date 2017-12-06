"""
.. module:: test_factories
"""

import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from apps.volontulo.factories import (
    UserFactory, OrganizationFactory, OfferFactory
    )
from apps.volontulo.models import Organization, Offer


class UserFactoryTestCase(TestCase):
    """Test for UserFactory."""
    def setUp(self):
        """setting up each test."""
        UserFactory.create(first_name='nie-Jan', last_name='nie-Kowalski')
        self.totally_fake_user = UserFactory.create()

    def test_factories_write_to_db(self):
        """Testing if UserFactory properly create fake user."""
        self.assertEqual(User.objects.count(), 2)

    def test_UserFactory_firstname_lastname(self):
        """Testing if UserFactory first_name fits to last_name."""
        tested_user = User.objects.get(first_name='nie-Jan')
        self.assertEqual(tested_user.last_name, 'nie-Kowalski')

    def test_UserFactory_faker_if_first_last_name_is_str(self):
        """Testing if created user.first_name,last_name is str and char>0."""
        self.assertTrue(isinstance(self.totally_fake_user.first_name, str))
        self.assertTrue(isinstance(self.totally_fake_user.last_name, str))
        self.assertTrue(len(self.totally_fake_user.first_name) > 0)
        self.assertTrue(len(self.totally_fake_user.last_name) > 0)

    def test_userfactory_faker_if_email_has_at(self):
        """Testing if email of last created user contains an @. """
        self.assertIn('@', self.totally_fake_user.email)

    def test_userfactory_faker_email_is_the_same_as_username(self):
        """Testing if email equals user_name."""
        self.assertEqual(
            self.totally_fake_user.email,
            self.totally_fake_user.username
            )


class OrganizationFactoryTestCase(TestCase):
    """Test for OrganizationFactory."""
    def setUp(self):
        """Set up each test"""
        OrganizationFactory.create(
            name='Flota zjednoczonych sił',
            address='Psia Wólka'
            )
        self.fake_organization = OrganizationFactory.create()

    def test_organizationfactory(self):
        """Testing if OrganizationFactory.create creates new Organization."""
        test_organization = Organization.objects.get(
            name='Flota zjednoczonych sił'
        )
        self.assertEqual(test_organization.address, 'Psia Wólka')

    def test_organization_if_name_address_description_is_str(self):
        """Test if organization name/address/description is str and char>0."""
        self.assertTrue(isinstance(self.fake_organization.name, str))
        self.assertTrue(isinstance(self.fake_organization.address, str))
        self.assertTrue(isinstance(self.fake_organization.description, str))
        self.assertTrue(len(self.fake_organization.name) > 0)
        self.assertTrue(len(self.fake_organization.address) > 0)
        self.assertTrue(len(self.fake_organization.description) > 0)


class OfferFactoryTestCase(TestCase):
    """Test for OfferFactory."""

    def setUp(self):
        """Set up test for OfferFactory"""

        self.fake_user1 = UserFactory.create(
            first_name="Fake user first_name1",
            last_name="Fake user last_name1"
            )
        self.fake_user2 = UserFactory.create(
            first_name="Fake user first_name2",
            last_name="Fake user last_name2"
            )
        self.fake_offer1 = OfferFactory.create(volunteers=User.objects.all())
        self.fake_offer2 = OfferFactory.create(
            title="Jakiś tytuł",
            description="Zwięzły opis",
            organization__name="Nazwa odnośnej organizacji"
            )

    def Test_if_users_have_been_created(self):
        """Testing if fake users have been created."""
        self.assertTrue(len(User.objects.all()) == 2)

    def Test_if_fake_organization_has_been_created(self):
        """Testing fake organization created by SubFactory."""
        self.assertTrue(len(Organization.objects.all()) == 2)

    def Test_if_offer_has_been_created(self):
        """Testing if offer has been created."""
        created_offer = Offer.objects.get(title="Jakiś tytuł")
        self.assertEqual(created_offer.description, "Zwięzły opis")

    def Test_if_offer_is_connected_with_some_organization(self):
        """Testing if offer is connected with organization."""
        fake_offer_with_organization = Offer.objects.filter(
            title="Jakiś tytuł"
            )[0]
        self.assertTrue(
            fake_offer_with_organization.organization.name,
            "Nazwa odnośnej organizacji"
            )

    def Test_if_offer_is_connected_with_some_volonteer(self):
        """Testing if offer is connected with volunteer."""
        fake_offer = Offer.objects.all()[0]
        fake_offer_volunteers1 = fake_offer.volunteers.filter(
            first_name="Fake user first_name1"
            )
        connected_user1 = fake_offer_volunteers1[0]
        fake_offer_volunteers2 = fake_offer.volunteers.filter(
            first_name="Fake user first_name2"
            )
        connected_user2 = fake_offer_volunteers2[0]
        self.assertTrue(connected_user1.last_name, "Fake user last_name1")
        self.assertTrue(connected_user2.last_name, "Fake user last_name2")

    def test_offers_paragraph_is_str(self):
        """Testing if offers textFields are str and chr>0."""
        description = self.fake_offer1.description
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) > 0)
        requirements = self.fake_offer1.requirements
        self.assertIsInstance(requirements, str)
        self.assertTrue(len(requirements) > 0)
        time_commitment = self.fake_offer1.time_commitment
        self.assertIsInstance(time_commitment, str)
        self.assertTrue(len(time_commitment) > 0)
        time_commitment = self.fake_offer1.time_commitment
        self.assertIsInstance(time_commitment, str)
        self.assertTrue(len(time_commitment) > 0)
        title = self.fake_offer1.title
        self.assertIsInstance(title, str)
        self.assertTrue(len(title) > 0)
        time_period = self.fake_offer1.time_period
        self.assertIsInstance(time_period, str)
        self.assertTrue(len(time_period) > 0)
        location = self.fake_offer1.location
        self.assertIsInstance(location, str)
        self.assertTrue(len(location) > 0)

    def test_offers_boolean_fields(self):
        """Testing if offers booleanFields are 0 or 1."""
        self.assertIsInstance(self.fake_offer1.votes, bool)
        self.assertIsInstance(self.fake_offer1.reserve_recruitment, bool)
        self.assertIsInstance(self.fake_offer1.action_ongoing, bool)
        self.assertIsInstance(self.fake_offer1.constant_coop, bool)

    def test_offers_datatime_fields(self):
        """Testing if offers datatimeFields are proper type."""
        self.assertIsInstance(self.fake_offer1.started_at, datetime.datetime)
        self.assertIsInstance(self.fake_offer1.started_at, datetime.datetime)
        self.assertIsInstance(
            self.fake_offer1.recruitment_start_date,
            datetime.datetime
            )
        self.assertIsInstance(
            self.fake_offer1.reserve_recruitment_start_date,
            datetime.datetime
            )
        self.assertIsInstance(
            self.fake_offer1.reserve_recruitment_end_date,
            datetime.datetime
            )
        self.assertIsInstance(
            self.fake_offer1.action_start_date,
            datetime.datetime
            )
        self.assertIsInstance(
            self.fake_offer1.action_end_date,
            datetime.datetime
            )

    def test_offer_if_choices_takes_proper_values(self):
        """Testing if fields with choices takes proper values."""
        self.assertIn(
            self.fake_offer1.status_old,
            ['NEW', 'ACTIVE', 'SUSPENDED']
            )
        self.assertIn(
            self.fake_offer1.offer_status,
            ['Unpublished', 'Published', 'Rejected']
            )
        self.assertIn(
            self.fake_offer1.recruitment_status,
            ['Open', 'Supplemental', 'Closed']
            )
        self.assertIn(
            self.fake_offer1.action_status,
            ['Future', 'Ongoing', 'Finished']
            )

    def test_offer_if_integerField_are_proper_type(self):
        """Testing if integerField is int type."""
        self.assertIsInstance(self.fake_offer1.volunteers_limit, int)
        self.assertIsInstance(self.fake_offer1.reserve_volunteers_limit, int)
        self.assertIsInstance(self.fake_offer1.weight, int)
