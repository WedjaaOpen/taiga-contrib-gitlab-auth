# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json
import re 

from pprint import pprint

from collections import namedtuple
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taiga.base.connectors.exceptions import ConnectorBaseException


class GitLabApiError(ConnectorBaseException):
    pass

######################################################
## Data
######################################################
GITLAB_URL = getattr(settings, "GITLAB_URL", None)
GITLAB_APP_ID = getattr(settings, "GITLAB_APP_ID", None)
GITLAB_APP_SECRET = getattr(settings, "GITLAB_APP_SECRET", None)

API_RESOURCES_URLS = {
    "login": {
        "authorize": "oauth/authorize",
        "access-token": "oauth/token"
    },
    "user": {
        "profile": "api/v3/user"
    }
}

HEADERS = {"Accept": "application/json",}

AuthInfo = namedtuple("AuthInfo", ["access_token"])
User = namedtuple("User", ["id", "username", "full_name", "bio", "email"])
Email = namedtuple("Email", ["email", "is_primary"])


######################################################
## utils
######################################################

def _build_url(*args, **kwargs) -> str:
    """
    Return a valid url.
    """
    resource_url = API_RESOURCES_URLS
    for key in args:
        resource_url = resource_url[key]

    if kwargs:
        resource_url = resource_url.format(**kwargs)

    return urljoin(GITLAB_URL, resource_url)


def _get(url:str, headers:dict) -> dict:
    """
    Make a GET call.
    """
    response = requests.get(url, headers=headers)

    data = response.json()
    if response.status_code != 200:
        raise GitLabApiError({"status_code": response.status_code,
                                  "error": data.get("message", response.text)})
    return data

def _post(url:str, params:dict, headers:dict) -> dict:
    """
    Make a POST call.
    """

    preparedRequest = requests.Request('POST', url, files=params, headers=headers).prepare()
    response = requests.Session().send(preparedRequest)

    data = response.json()
    if response.status_code != 200 or "error" in data:
        raise GitLabApiError({"status_code": response.status_code,
                                  "error": data.get("error_description", response.text)})
    return data


######################################################
## Simple calls
######################################################

def login(access_code:str, redirect_uri:str, application_id:str=GITLAB_APP_ID, application_secret:str=GITLAB_APP_SECRET,
          headers:dict=HEADERS):
    """
    Get access_token fron an user authorized code, the GitLab application id and secret key.
    (See https://github.com/doorkeeper-gem/doorkeeper - the middleware used by  GitLab).
    """

    if not application_id:
        raise GitLabApiError({"error_message": _("Missing GITLAB_APP_ID from configuration.")})

    if not application_secret:
        raise GitLabApiError({"error_message": _("Missing GITLAB_APP_SECRET from configuration.")})

    if not GITLAB_URL:
        raise GitLabApiError({"error_message": _("Missing GITLAB_URL from configuration.")})

    authorized_redirect = re.sub(r'(?is)&code=.+', '', redirect_uri)

    url = urljoin(GITLAB_URL, "oauth/token")
    print("OAUTH: ", url, " - code: ", access_code, " - client id: ", application_id, "- secret: ", application_secret)
    params={"code": (None, access_code),
            "client_id": (None, application_id),
            "client_secret": (None, application_secret),
	    "grant_type": (None, "authorization_code"),
            "redirect_uri": (None, authorized_redirect)
	   }
    data = _post(url, params=params, headers=headers)
    return AuthInfo(access_token=data.get("access_token", None))


def get_user_profile(headers:dict=HEADERS):
    """
    Get authenticated user info.
    (See http://doc.gitlab.com/ce/api/users.html#for-normal-users).
    """
    url = _build_url("user", "profile")
    data = _get(url, headers=headers)
    return User(id=data.get("id", None),
		email=data.get("email", None),
                username=data.get("login", data.get("username", None)),
                full_name=(data.get("name", None) or ""),
                bio=(data.get("bio", None) or ""))


######################################################
## Convined calls
######################################################

def me(access_code:str, redirect_uri:str) -> tuple:
    """
    Connect to a gitlab account and get all personal info (profile and the primary email).
    """
    auth_info = login(access_code, redirect_uri)

    headers = HEADERS.copy()
    headers["Authorization"] = "Bearer {}".format(auth_info.access_token)

    print ("Authorization: ", headers["Authorization"]);
    user = get_user_profile(headers=headers)
    return user.email, user

