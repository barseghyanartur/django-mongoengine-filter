from mongoengine import fields, document
from .constants import PROFILE_TYPES, PROFILE_TYPE_FREE, GENDERS, GENDER_MALE

__all__ = ("Person",)


class Person(document.Document):

    name = fields.StringField(
        required=True, max_length=255, default="Robot", verbose_name="Name"
    )
    age = fields.IntField(required=True, verbose_name="Age")
    num_fingers = fields.IntField(required=False, verbose_name="Number of fingers")
    profile_type = fields.StringField(
        required=False,
        blank=False,
        null=False,
        choices=PROFILE_TYPES,
        default=PROFILE_TYPE_FREE,
    )
    gender = fields.StringField(
        required=False, blank=False, null=False, choices=GENDERS, default=GENDER_MALE
    )

    def __str__(self):
        return self.name
