from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from mongoengine import connect

from .dfm_app.constants import (
    GENDER_FEMALE,
    GENDER_MALE,
    PROFILE_TYPE_FREE,
    PROFILE_TYPE_MEMBER,
)
from .factories import PersonFactory

__all__ = ("FiltersTest",)

db = connect("test")
db.drop_database("test")


class FiltersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()
        cls.client = Client()
        cls.person_free_male = PersonFactory(
            name="Free male",
            profile_type=PROFILE_TYPE_FREE,
            gender=GENDER_MALE,
            num_fingers=11,
        )
        cls.person_free_female = PersonFactory(
            name="Free female",
            profile_type=PROFILE_TYPE_FREE,
            gender=GENDER_FEMALE,
            num_fingers=10,
        )
        cls.person_member_female = PersonFactory(
            name="Member female",
            profile_type=PROFILE_TYPE_MEMBER,
            gender=GENDER_FEMALE,
            num_fingers=10,
        )
        cls.url = reverse("person_list")
        cls.url_cbv = reverse("person_list_cbv")
        super(FiltersTest, cls).setUpClass()

    def _test_base(self, url):
        # All
        response_all = self.client.get(url)
        soup_all = BeautifulSoup(
            getattr(response_all, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_all.find_all("li")), 3)

        # Free male
        response_free_male = self.client.get(
            "{url}?profile_type={profile_type}&gender={gender}".format(
                url=url, profile_type=PROFILE_TYPE_FREE, gender=GENDER_MALE
            )
        )
        soup_free_male = BeautifulSoup(
            getattr(response_free_male, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_free_male.find_all("li")), 2)

        # Free female
        response_free_female = self.client.get(
            "{url}?profile_type={profile_type}&gender={gender}".format(
                url=url, profile_type=PROFILE_TYPE_FREE, gender=GENDER_FEMALE
            )
        )
        soup_free_female = BeautifulSoup(
            getattr(response_free_female, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_free_female.find_all("li")), 2)

        # Member female
        response_member_female = self.client.get(
            "{url}?profile_type={profile_type}&gender={gender}".format(
                url=url, profile_type=PROFILE_TYPE_MEMBER, gender=GENDER_FEMALE
            )
        )
        soup_member_female = BeautifulSoup(
            getattr(response_member_female, "content", ""),
            features="html.parser",
        )
        self.assertEqual(len(soup_member_female.find_all("li")), 1)

        # Custom method
        response_ten_fingers = self.client.get(
            "{url}?ten_fingers=yes".format(url=url)
        )
        soup_ten_fingers = BeautifulSoup(
            getattr(response_ten_fingers, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_ten_fingers.find_all("li")), 2)

        # Agnostic
        response_agnostic = self.client.get(
            "{url}?agnostic=True".format(url=url)
        )
        soup_all = BeautifulSoup(
            getattr(response_agnostic, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_all.find_all("li")), 3)

        # Not Agnostic
        response_agnostic = self.client.get(
            "{url}?agnostic=False".format(url=url)
        )
        soup_all = BeautifulSoup(
            getattr(response_agnostic, "content", ""), features="html.parser"
        )
        self.assertEqual(len(soup_all.find_all("li")), 0)

    def test_base(self):
        return self._test_base(self.url)

    def test_base_cbv(self):
        return self._test_base(self.url_cbv)
