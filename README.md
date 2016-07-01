Taiga contrib gitlab auth
=========================

The Taiga plugin for gitlab authentication.

Installation
------------
### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-gitlab-auth` with:

```bash
  pip install taiga-contrib-gitlab-auth
```

Modify your `settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_gitlab_auth"]

  # Create an application in GitLab - "/admin/applications"
  GITLAB_URL = "https://your.gitlab.access.com"
  GITLAB_APP_ID = "YOUR-GITHUB-CLIENT-ID"
  GITLAB_APP_SECRET = "YOUR-GITHUB-CLIENT-SECRET"
```

#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-gitlab-auth` compiled code (you need subversion in your system):

```bash
  cd dist/
  mkdir -p plugins
  cd plugins
  svn export "https://github.com/WedjaaOpen/taiga-contrib-gitlab-auth/tags/$(pip show taiga-contrib-gitlab-auth | awk '/^Version: /{print $2}')/front/dist"  "gitlab-auth"
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/gitlab-auth/gitlab-auth.json"`:

```json
...
    "gitLabAppId": "YOUR-GITLAB-APP-ID",
    "gitLabUrl": "https://your.gitlab.com",
    "contribPlugins": [
        (...)
        "/plugins/gitlab-auth/gitlab-auth.json"
    ]
...
```

### Dev env

#### Taiga Back

Clone the repo and

```bash
  cd taiga-contrib-gitlab-taiga/back

  workon taiga
  pip install -e .
```

Modify `taiga-back/settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_gitlab_auth"]

  # Create an application in GitLab - "/admin/applications"
  GITLAB_URL = "https://your.gitlab.access.com"
  GITLAB_APP_ID = "YOUR-GITHUB-CLIENT-ID"
  GITLAB_APP_SECRET = "YOUR-GITHUB-CLIENT-SECRET"
```

#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-gitlab-auth/dist gitlab-auth
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/gitlab-auth/gitlab-auth.json"`:

```json
...
    "gitLabAppId": "YOUR-GITHUB-APP-ID",
    "gitLabUrl": "https://your.gitlab.com",
    "contribPlugins": [
        (...)
        "/plugins/gitlab-auth/gitlab-auth.json"
    ]
...
```

In the plugin source dir `taiga-contrib-gitlab-auth/front` run

```bash
npm install
```
and use:

- `gulp` to regenerate the source and watch for changes.
- `gulp build` to only regenerate the source.

Running tests
-------------

We only have backend tests, you have to add your `taiga-back` directory to the
PYTHONPATH environment variable, and run py.test, for example:

```bash
  cd back
  add2virtualenv /home/taiga/taiga-back/
  py.test
```

