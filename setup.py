from setuptools import setup, find_packages

f = open("README.rst")
readme = f.read()
f.close()

setup(
    name="django-mongoengine-filter",
    version="0.1",
    description=(
        "django-mongoengine-filter is a reusable Django application inspired "
        "from django-filter for allowing mongoengine users to filter querysets "
        "dynamically."
    ),
    long_description=readme,
    author="Artur Barseghyhan",
    author_email="artur.barseghyan@gmail.com",
    url="https://github.com/barseghyanartur/django-mongoengine-filter",
    packages=find_packages(exclude=["tests"]),
    package_data={"django_filters_mongoengine": ["locale/*/LC_MESSAGES/*"]},
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Framework :: Django",
    ],
    include_package_data=True,
    zip_safe=False,
)
