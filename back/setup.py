#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-gitlab-auth',
    version = ":versiontools:taiga_contrib_gitlab_auth:",
    description = "The Taiga plugin for gitlab authentication",
    long_description = "",
    keywords = 'taiga, gitlab, auth, plugin',
    author = 'Fabio "MrWHO" Torchetti',
    author_email = 'mrwho@wedjaa.net',
    url = 'https://github.com/WedjaaOpen/taiga-contrib-gitlab-auth',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
