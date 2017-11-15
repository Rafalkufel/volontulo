from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase

from apps.volontulo.factories.factories import UserFactory, OrganizationFactory
from apps.volontulo.models import Organization


class UserFactoryTestCase(TestCase):
    def setUp(self):
        u"""setting up each test"""
        # create user
        UserFactory.create(first_name="Kornik", last_name="WDrzewie")
        # create fake user
        UserFactory.create()
        self.last_add_user = User.objects.last()
        
    def test_userfactory_firstname_lastname(self):
        """test wether UserFactory first_name fits to last_name"""
        tested_user = User.objects.get(first_name='Kornik')
        self.assertEqual(tested_user.last_name, 'WDrzewie')

    def test_userfactory_faker_if_first_last_name_is_str(self):
        """test wether last created user.first_name,last_name is str
        and has more than 0 char"""
        # last_add_user = User.objects.last()
        self.assertTrue(isinstance(self.last_add_user.first_name, str))
        self.assertTrue(isinstance(self.last_add_user.last_name, str))
        self.assertTrue(len(self.last_add_user.first_name) > 0)
        self.assertTrue(len(self.last_add_user.last_name) > 0)

    def test_userfactory_faker_if_email_has_at(self):
        """test wether email of last created user has an @ """
        self.assertTrue(self.last_add_user.email.find('@') >= 0)

    def test_userfactory_faker_email_is_the_same_as_username(self):
        """test if email equals user_name"""
        self.assertEqual(
            self.last_add_user.email,
            self.last_add_user.username
            )


class OrganizationFactoryTestCase(TestCase):
    def setUp(self):
        """Set up each test"""
        # test if organization is created
        OrganizationFactory.create(
            name='Flota zjednoczonych sił', 
            address='Psia Wólka'
            )

        # test fakes names, address, description
        OrganizationFactory.create()
        self.fake_organization = Organization.objects.last()

    def test_organizationfactory(self):
        """test if OrganizationFactory.create creates new Organization"""
        test_organization = Organization.objects.get(name='Flota zjednoczonych sił')
        self.assertEqual(test_organization.address, 'Psia Wólka')

    def test_organization_if_name_address_description_is_str(self):
        """check if organization name/address/description is str
        and has more than zero char"""
        self.assertTrue(isinstance(self.fake_organization.name, str))
        self.assertTrue(isinstance(self.fake_organization.address, str))
        self.assertTrue(isinstance(self.fake_organization.description, str))
        self.assertTrue(len(self.fake_organization.name) > 0)
        self.assertTrue(len(self.fake_organization.address) > 0)
        self.assertTrue(len(self.fake_organization.description) > 0)
