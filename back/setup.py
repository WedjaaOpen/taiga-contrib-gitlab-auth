#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from taiga_contrib_gitlab_auth import __version__
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-gitlab-auth',
    version = '.'.join(map(str,__version__)),
    description = "The Taiga plugin for gitlab authentication",
    long_description = "This plugin allows integration with a GitLab installation",
    keywords = 'taiga, gitlab, auth, plugin',
    author = 'Fabio "MrWHO" Torchetti',
    author_email = 'mrwho@wedjaa.net',
    url = 'https://github.com/WedjaaOpen/taiga-contrib-gitlab-auth',
    download_url = 'https://github.com/WedjaaOpen/taiga-contrib-gitlab-auth/tarball/' + '.'.join(map(str,__version__)),
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
