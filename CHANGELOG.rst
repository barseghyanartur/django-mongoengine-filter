Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.4.2
-----
2023-05-24

- Fix `AttributeError: 'BaseFilterSet' object has no attribute 'is_valid'` issue.

0.4.1
-----
2023-02-23

- Fix issue with adding ``help_text``.

0.4.0
-----
2022-12-24

- Drop support for Python < 3.7.
- Drop support for Django < 2.2.
- Tested against Python 3.9, 3.10 and 3.11.
- Tested against Django 3.1, 3.2, 4.0 and 4.1.
- Apply ``black``, ``isort`` and ``ruff``.
- Fix GitHub CI.

0.3.5
-----
2020-03-23

- Tested against Python 3.8.
- Tested against Django 3.0.

0.3.4
-----
2019-04-04

- Using lazy queries where possible.

0.3.3
-----
2019-04-02

- Tested against Django 2.2.

0.3.2
-----
2019-04-01

- Fixes in class-based views.
- Addition to docs.

0.3.1
-----
2019-03-26

- More tests.
- Addition to docs.

0.3
---
2019-03-25

*Got status beta*

.. note::

    Namespace changed from `django_filters_mongoengine` to
    `django_mongoengine_filter`. Modify your imports accordingly.

- Clean up.
- Added docs, manifest, tox.

0.2
---
2019-03-25

- Working method filters.

0.1
---
2019-03-25

- Initial alpha release.
