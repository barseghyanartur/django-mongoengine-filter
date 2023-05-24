from setuptools import find_packages, setup

with open("README.rst", "r") as _file:
    readme = _file.read()

install_requires = [
    "six>=1.9",
]

extras_require = []

tests_require = [
    "factory_boy",
    "fake-factory",
    "pytest",
    "pytest-django",
    "pytest-cov",
    "tox",
]

setup(
    name="django-mongoengine-filter",
    version="0.4.2",
    description=(
        "django-mongoengine-filter is a reusable Django application inspired "
        "from django-filter for allowing mongoengine users to filter querysets "
        "dynamically."
    ),
    long_description=readme,
    keywords="mongoengine, django-filter",
    author="Artur Barseghyhan",
    author_email="artur.barseghyan@gmail.com",
    url="https://github.com/barseghyanartur/django-mongoengine-filter",
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/"
        "django-mongoengine-filter/issues",
        "Documentation": "https://django-mongoengine-filter.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/"
        "django-mongoengine-filter",
        "Changelog": "https://django-mongoengine-filter.readthedocs.io/"
        "en/latest/changelog.html",
    },
    packages=find_packages(exclude=["tests"]),
    package_data={"django_mongoengine_filter": ["locale/*/LC_MESSAGES/*"]},
    license="GPL-2.0-only OR LGPL-2.1-or-later",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
    ],
    python_requires=">=3.7",
    install_requires=(install_requires + extras_require),
    tests_require=tests_require,
    include_package_data=True,
    zip_safe=False,
)
