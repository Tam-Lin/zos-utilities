=======
zos-utilities
=======


.. image:: https://img.shields.io/pypi/v/zos-utilities.svg
        :target: https://pypi.python.org/pypi/zos-utilities
        :alt:  Pypi

.. image:: https://github.com/Tam-Lin/zos-utilities/actions/workflows/build.yml/badge.svg
        :target: https://github.com/Tam-Lin/zos-utilities/actions/workflows/build.yml
        :alt: Build Status

.. image:: https://readthedocs.org/projects/zos-utilities/badge/?version=latest
        :target: https://zos-utilities.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Library for performing various utility functions needed for z/OS libraries.  Right now, this just means "Julian"
date conversion.  But I have a couple of libraries that do various things for/with z/OS, and they all need
to convert from the z/OS Julian Date to datetime, so I thought I might as well put it into a library.