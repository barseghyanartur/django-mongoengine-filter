import os
import unittest

from bs4 import BeautifulSoup

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
import django

django.setup()

from faker import Faker

from mongoengine import connect

from django.test import TestCase, Client

from .dfm_app.constants import (
    GENDER_MALE,
    GENDER_FEMALE,
    PROFILE_TYPE_FREE,
    PROFILE_TYPE_MEMBER,
)
from .factories import *

__all__ = ("FitlersTest",)

db = connect("test")
db.drop_database("test")


class FitlersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()
        cls.client = Client()
        cls.person_free_male = PersonFactory(
            name="Free male",
            profile_type=PROFILE_TYPE_FREE,
            gender=GENDER_MALE
        )
        cls.person_free_female = PersonFactory(
            name="Free female",
            profile_type=PROFILE_TYPE_FREE,
            gender=GENDER_FEMALE,
            num_fingers=10
        )
        cls.person_member_female = PersonFactory(
            name="Member female",
            profile_type=PROFILE_TYPE_MEMBER,
            gender=GENDER_FEMALE,
            num_fingers=10
        )
        super(FitlersTest, cls).setUpClass()

    def test_base(self):
        # All
        response_all = self.client.get("/persons/")
        soup_all = BeautifulSoup(
            getattr(response_all, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_all.find_all("li")), 3)

        # Free male
        response_free_male = self.client.get(
            "/persons/?profile_type={profile_type}&gender={gender}".format(
                profile_type=PROFILE_TYPE_FREE, gender=GENDER_MALE
            )
        )
        soup_free_male = BeautifulSoup(
            getattr(response_free_male, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_free_male.find_all("li")), 2)

        # Free female
        response_free_female = self.client.get(
            "/persons/?profile_type={profile_type}&gender={gender}".format(
                profile_type=PROFILE_TYPE_FREE, gender=GENDER_FEMALE
            )
        )
        soup_free_female = BeautifulSoup(
            getattr(response_free_female, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_free_female.find_all("li")), 2)

        # Member female
        response_member_female = self.client.get(
            "/persons/?profile_type={profile_type}&gender={gender}".format(
                profile_type=PROFILE_TYPE_MEMBER, gender=GENDER_FEMALE
            )
        )
        soup_member_female = BeautifulSoup(
            getattr(response_member_female, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_member_female.find_all("li")), 1)

        # Custom method
        response_ten_fingers = self.client.get("/persons/?ten_fingers=yes")
        soup_ten_fingers = BeautifulSoup(
            getattr(response_ten_fingers, "content", ""),
            features="html.parser"
        )
        self.assertEqual(len(soup_ten_fingers.find_all("li")), 2)


if __name__ == "__main__":
    unittest.main()
