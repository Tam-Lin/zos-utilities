0.1.0 (2022-04-20)
------------------

* First release on PyPI.

0.2.0 (2022-05-02)
----------------------
* Add initial support for CPCs, LPARs, and logical CPUs
* Change minimum python level to 3.7 so I can use dataclasses.  3.6 is EOL anyway.

0.3.0 (2022-05-04)
----------------------
* Add support for PROCVIEW CPU systems

0.3.1 (2022-05-04)
----------------------
* Had conflicting requirements for twine in requirements_dev.txt

0.4.0 (2022-05-10)
----------------------
* Add some additional cpc and lpar fields
* Automate build and publishing to Pypi

0.5.0 (2022-05-25)
----------------------
* Strip out leading spaces from inputs (because sometimes they're getting passed in that way)

0.5.3 (2022-06-13)
----------------------
* Bugfixes

0.6.0 (2023-06-25)
----------------------
* Add initial support for IEE200I (D ASM output)
