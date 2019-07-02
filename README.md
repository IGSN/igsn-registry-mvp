# isgn-registry-mvp
IGSN registry provider MVP: Lightweight submission verification (too lightweight - we need to replace this with a Batch workflow as it's killing us to do deploys in this way).

_add badges here_

### Installing dependencies

We're using pipenv to make this easy. If you already have a system Python installed, you should be able to do:


```bash
$ pip install pipenv
```

or alternatively on MacOS

```bash
$ brew install pipenv
```

and then configure dependencies and a virtualenv using

```bash
$ pipenv install
Running $ pipenv lock then $ pipenv sync.
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
✔ Success!
Updated Pipfile.lock (3ce347)!
Installing dependencies from Pipfile.lock (3ce347)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 39/39 — 00:00:23
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
All dependencies are now up-to-date!
```

You can then run the test flask server using

```bash
$  pipenv shell "export FLASK_APP=api:create_app; flask run --port 8182"  # or whatever
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8182/ (Press CTRL+C to quit)
```

and start making requests (I recommend `pip instal httpie`)

```bash
$ http :8182/igsn/foo
```

or posting JSON:

```bash
$ http --json POST :8182/score bucket="unearthed-portal-lambda-dev" submission_filename="explorer/example_submission_optimist.csv"
HTTP/1.0 200 OK
Content-Length: 62
Content-Type: application/json
Date: Mon, 29 Apr 2019 03:51:03 GMT
Server: Werkzeug/0.14.1 Python/3.6.8

{
    "private": 0.3440113354825938,
    "public": 0.3440113354825938
}
```

### Testing and development

If you're going to run the tests then you need to install all the development packages:

```bash
$ pipenv install --dev
# snip pipenv output
```

and then we can run `pytest`:

```bash
$ pipenv run pytest
# pytest output follows...
```

There's a few doctests for simple functions, and then most tests live in the `tests` folder.

### Deploy

We just deploy with zappa. Prior to deploying you probably want to remove all the dev
packages from the virtualenv (otherwise you'll be well over the 50 Mb lambda limit). Note that `pipenv uninstall --dev` [doesn't work at time of writing but might have changed](https://github.com/pypa/pipenv/issues/3385) so we do a full uninstall/reinstall as a workaround.

```bash
$ pipenv uninstall --all
$ pipenv install   # won't install dev
```

Then we can deploy/update/undeploy etc etc

```bash
$ pipenv run zappa deploy dev  # or update or prod
# snip output
```

**Note that if you are doing a clean deploy you will have to go to AWS API Gateway > Usage Plans and add the 'portal' API key to the gateway.**

If you need to see the status of your function you can do

```bash
$ zappa status
```