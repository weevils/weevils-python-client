# -*- coding: utf-8 -*-
"""
Client library for use with the weevils.io API
"""
from setuptools import find_packages, setup

LONG_DESCRIPTION = open("README.rst").read() + "\n" + open("CHANGELOG.md").read()
VERSION = "0.0.4"

setup(
    name="weevils",
    author="weevils.io",
    author_email="code@weevils.io",
    url="https://weevils.io",
    description="A client library for using the weevils.io API",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests==2.21.0", "requests-oauthlib==1.2.0"],
    extras_require={
        "for_tests": ["pytest==4.2.1", "betamax==0.8.1"],
        "for_dev": ["pre-commit==1.14.3", "prospector==1.1.6.2"],
    },
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["weevils", "api", "client"],
    zip_safe=False,
)
