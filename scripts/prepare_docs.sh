#!/usr/bin/env bash
cat README.rst docs/documentation.rst.distrib > docs/index.rst
cat CHANGELOG.rst > docs/changelog.rst
cat docs/filters.rst.distrib > docs/filters_doc.rst
cat docs/widgets.rst.distrib > docs/widgets_doc.rst
