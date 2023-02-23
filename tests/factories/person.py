import factory
import factory.fuzzy
from dfm_app.constants import GENDERS, PROFILE_TYPES
from dfm_app.documents import Person

__all__ = ("PersonFactory",)


def build_factory(cls, specified_fields=None):
    return factory.build(
        dict, FACTORY_CLASS=cls, **specified_fields if specified_fields else {}
    )


class PersonFactory(factory.mongoengine.MongoEngineFactory):
    name = factory.Faker("word")
    age = factory.Faker("pyint")
    num_fingers = factory.Faker("pyint")
    profile_type = factory.fuzzy.FuzzyChoice(choices=PROFILE_TYPES)
    gender = factory.fuzzy.FuzzyChoice(choices=GENDERS)

    class Meta:
        model = Person
